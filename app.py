import csv, io, os, re, secrets, sqlite3
from collections import defaultdict, deque
from datetime import datetime, timezone
from functools import wraps
from contextlib import contextmanager
from pathlib import Path
import bcrypt
from dotenv import load_dotenv
from flask import Flask, Response, abort, jsonify, request, send_from_directory, session

load_dotenv(); BASE_DIR=Path(__file__).resolve().parent; DATABASE=BASE_DIR/'data'/'tanishi.db'; BUCKETS=defaultdict(deque); RATE_RULES={'/api/admin/login':(15,300),'/api/enquiries':(5,3600)}
app=Flask(__name__,static_folder=None)
app.config.update(SECRET_KEY=os.getenv('FLASK_SECRET_KEY',''),SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',SESSION_COOKIE_SECURE=os.getenv('COOKIE_SECURE','false').lower()=='true',MAX_CONTENT_LENGTH=16*1024)
if not app.config['SECRET_KEY']: raise RuntimeError('Set FLASK_SECRET_KEY in .env. See .env.example.')
@contextmanager
def db():
 DATABASE.parent.mkdir(exist_ok=True); con=sqlite3.connect(DATABASE); con.row_factory=sqlite3.Row
 try:
  yield con; con.commit()
 finally:
  con.close()
def init_db():
 with db() as con: con.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT PRIMARY KEY,name TEXT NOT NULL,mobile TEXT NOT NULL,service TEXT NOT NULL,city TEXT,message TEXT,consent_at TEXT NOT NULL,status TEXT NOT NULL DEFAULT "New",created_at TEXT NOT NULL)')
init_db()
def clean(value,limit=500): return re.sub(r'[<>]','',str(value or '')).strip()[:limit]
def stamp(): return datetime.now(timezone.utc).isoformat()
def limited():
 # Local development must never lock the developer out; production enables the limiter via COOKIE_SECURE=true.
 if not app.config['SESSION_COOKIE_SECURE']: return False
 limit,window=RATE_RULES.get(request.path,(20,300)); bucket=BUCKETS[f"{request.path}:{request.remote_addr or 'unknown'}"]; cutoff=datetime.now().timestamp()-window
 while bucket and bucket[0]<cutoff: bucket.popleft()
 if len(bucket)>=limit:return True
 bucket.append(datetime.now().timestamp());return False
def admin_only(fn):
 @wraps(fn)
 def wrapped(*args,**kwargs):
  if not session.get('admin_authenticated'): return jsonify(error='Authentication required.'),401
  return fn(*args,**kwargs)
 return wrapped
@app.after_request
def headers(response):
 response.headers['X-Content-Type-Options']='nosniff';response.headers['X-Frame-Options']='DENY';response.headers['Referrer-Policy']='strict-origin-when-cross-origin';response.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()';response.headers['Content-Security-Policy']="default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'self'; frame-ancestors 'none'"
 if request.path in {'/admin.html','/js/admin.js'}: response.headers['Cache-Control']='no-store'
 return response
@app.get('/')
def home(): return send_from_directory(BASE_DIR,'index.html')
@app.get('/healthz')
def health(): return jsonify(status='ok')
@app.get('/favicon.ico')
def favicon(): return send_from_directory(BASE_DIR,'favicon.svg')
@app.get('/<path:name>')
def static(name):
 public_files={'index.html','admin.html','privacy.html','robots.txt','sitemap.xml','favicon.svg'}
 if name not in public_files and not name.startswith(('css/','js/')): abort(404)
 return send_from_directory(BASE_DIR,name)
@app.post('/api/enquiries')
def enquiry():
 if not request.is_json:return jsonify(error='JSON request required.'),415
 if limited():return jsonify(error='Too many submissions. Please try again later.'),429
 p=request.get_json(silent=True) or {}
 if p.get('website'):return jsonify(reference_id='TF-RECEIVED'),201
 name,mobile,service=clean(p.get('name'),80),re.sub(r'\D','',str(p.get('mobile',''))),clean(p.get('service'),80)
 if not name or not service or not re.fullmatch(r'[6-9]\d{9}',mobile):return jsonify(error='Provide a name, valid mobile number and service.'),400
 if p.get('consent') is not True:return jsonify(error='Consent is required.'),400
 ident=f"TF-{datetime.now().strftime('%y%m%d')}-{secrets.token_hex(3).upper()}"
 with db() as con:con.execute('INSERT INTO leads VALUES(?,?,?,?,?,?,?,?,?)',(ident,name,mobile,service,clean(p.get('city'),60),clean(p.get('message')),stamp(),'New',stamp()))
 return jsonify(reference_id=ident),201
@app.post('/api/admin/login')
def login():
 if not request.is_json:return jsonify(error='JSON request required.'),415
 if limited():return jsonify(error='Too many attempts. Please try again later.'),429
 p=request.get_json(silent=True) or {}; valid=bool(os.getenv('ADMIN_USERNAME') and os.getenv('ADMIN_PASSWORD_HASH') and secrets.compare_digest(clean(p.get('username'),80),os.getenv('ADMIN_USERNAME','')))
 try:valid=valid and bcrypt.checkpw(str(p.get('password','')).encode(),os.getenv('ADMIN_PASSWORD_HASH','').encode())
 except ValueError:valid=False
 if not valid:return jsonify(error='Invalid credentials.'),401
 session.clear();session['admin_authenticated']=True;return jsonify(ok=True)
@app.post('/api/admin/logout')
@admin_only
def logout():session.clear();return jsonify(ok=True)
@app.get('/api/admin/leads')
@admin_only
def leads():
 with db() as con:rows=con.execute('SELECT id,name,mobile,service,city,message,status,created_at FROM leads ORDER BY created_at DESC').fetchall()
 return jsonify(leads=[dict(x) for x in rows])
@app.patch('/api/admin/leads/<lead_id>')
@admin_only
def update(lead_id):
 if not request.is_json:return jsonify(error='JSON request required.'),415
 status=clean((request.get_json(silent=True)or{}).get('status'),20)
 if status not in {'New','Contacted','Documents','Sanction','Disbursed','Rejected','Closed'}:return jsonify(error='Invalid lead status.'),400
 with db() as con:result=con.execute('UPDATE leads SET status=? WHERE id=?',(status,lead_id))
 if result.rowcount==0:return jsonify(error='Lead not found.'),404
 return jsonify(ok=True)
@app.get('/api/admin/leads.csv')
@admin_only
def export():
 with db() as con:rows=con.execute('SELECT id,name,mobile,service,city,message,status,created_at FROM leads ORDER BY created_at DESC').fetchall()
 out=io.StringIO();writer=csv.writer(out);writer.writerow(['Lead ID','Name','Mobile','Service','City','Message','Status','Created at']);writer.writerows([[r[k] for k in r.keys()]for r in rows]);return Response(out.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=tanishi-finance-leads.csv'})
if __name__=='__main__':
 print('Tanishi Finance local server: http://127.0.0.1:5055')
 init_db();app.run(host='127.0.0.1',port=5055,debug=False)

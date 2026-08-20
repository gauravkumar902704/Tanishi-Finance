import os
import tempfile
import unittest
import bcrypt

os.environ['FLASK_SECRET_KEY'] = 'test-secret-key-only'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD_HASH'] = bcrypt.hashpw(b'correct-password', bcrypt.gensalt()).decode()

import app

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp.close()
        app.DATABASE = app.Path(self.temp.name)
        app.init_db()
        self.client = app.app.test_client()

    def test_health_and_home(self):
        self.assertEqual(self.client.get('/healthz').status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response.close()
        favicon = self.client.get('/favicon.ico')
        self.assertEqual(favicon.status_code, 200)
        favicon.close()
        self.assertEqual(self.client.get('/.env').status_code, 404)
        self.assertEqual(self.client.get('/app.py').status_code, 404)

    def test_rejects_invalid_enquiry(self):
        self.assertEqual(self.client.post('/api/enquiries', json={}).status_code, 400)
        self.assertEqual(self.client.post('/api/enquiries', data='bad').status_code, 415)

    def test_creates_enquiry_and_protects_admin(self):
        response = self.client.post('/api/enquiries', json={'name':'Asha','mobile':'9876543210','service':'Personal Loan','consent':True})
        self.assertEqual(response.status_code, 201)
        self.assertIn('reference_id', response.json)
        self.assertEqual(self.client.get('/api/admin/leads').status_code, 401)
        self.assertEqual(self.client.post('/api/admin/login', json={'username':'admin','password':'correct-password'}).status_code, 200)
        self.assertEqual(self.client.get('/api/admin/leads').status_code, 200)
        lead_id = response.json['reference_id']
        self.assertEqual(self.client.patch(f'/api/admin/leads/{lead_id}', json={'status':'Contacted'}).status_code, 200)
        exported = self.client.get('/api/admin/leads.csv')
        self.assertEqual(exported.status_code, 200)
        self.assertIn(lead_id, exported.get_data(as_text=True))
        self.assertEqual(self.client.post('/api/admin/logout').status_code, 200)
        self.assertEqual(self.client.get('/api/admin/leads').status_code, 401)

if __name__ == '__main__':
    unittest.main()

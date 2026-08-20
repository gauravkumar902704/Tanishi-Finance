# Free deployment checklist

This project can run free on your own Windows PC or a free-tier Python host. A public deployment always requires an account you control, so credentials and DNS changes cannot be performed from this workspace.

1. Create `.env` from `.env.example`; generate a unique secret and bcrypt password hash.
2. Set `COOKIE_SECURE=true` only when HTTPS is active.
3. Use a production WSGI server, not `python app.py`. For example: `waitress-serve --listen=0.0.0.0:8000 app:app`.
4. Set a persistent disk/database, daily backup job, and a separate backup destination.
5. Replace every `tanishifinance.example` value in `index.html`, `robots.txt`, and `sitemap.xml` with the verified live domain.
6. Add a free CAPTCHA provider only if spam volume requires it; the included honeypot and rate limiter work without a third-party account.
7. Obtain written approval for lender logos, claims, rates, address, phone number, privacy terms and consent wording before publishing.

## Local free run

`python -m pip install -r requirements.txt`

`python app.py`

Open `http://127.0.0.1:5055/`.

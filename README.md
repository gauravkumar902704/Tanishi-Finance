# Tanishi Finance

Clean, static front-end for Tanishi Finance. Open `index.html` with a local web server (for example VS Code Live Server) so ES modules work reliably.

## Project layout

- `css/variables.css` — design tokens
- `css/style.css` — base, layout and components
- `css/responsive.css` — mobile/tablet rules
- `js/app.js` — page interactions and modal
- `js/emi.js` — pure EMI calculation
- `js/validation.js` — input sanitisation and validation

## Audit summary

The supplied legacy file is retained unchanged as a reference. It contains nine style blocks, 97 `!important` declarations, 51 inline event handlers, and a 3 MB Base64 logo. `index.html` replaces that structure with semantic HTML, external CSS/JS, responsive navigation, accessible modal form, client-side validation, SEO metadata/schema and an EMI calculator.

## Run locally

1. Copy `.env.example` to `.env`, then set a long random `FLASK_SECRET_KEY` and a bcrypt `ADMIN_PASSWORD_HASH`.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Run: `python app.py`
4. Open `http://127.0.0.1:5055/`. Staff can use `/admin.html` after configured credentials are set.

## Free operations included

- Run API checks: `python -m unittest tests/test_api.py`
- Verify admin configuration: `python scripts/verify_admin_config.py`
- Reset the admin password securely: `python scripts/reset_admin_password.py`
- Check server health: `http://127.0.0.1:5055/healthz`
- Create a local backup: `python scripts/backup.py`
- Use Windows Task Scheduler to run the backup script daily. Keep backups outside the deployment machine for recovery.

## Before production launch

The included Flask API provides server-side validation, rate limiting, a honeypot, consent capture, SQLite storage and an authenticated admin dashboard. Deploy it behind HTTPS with a production WSGI server, a managed database, backups, monitoring and a real CAPTCHA provider. Do not use the built-in Flask server or SQLite for a public high-volume deployment. Replace the placeholder canonical URLs and complete legal/lender verification before publishing.

See `DEPLOYMENT.md` for the zero-cost local/free-tier deployment checklist.

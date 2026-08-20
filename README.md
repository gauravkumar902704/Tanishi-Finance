# 🚀 Tanishi Finance

> A modern, secure, and responsive financial services platform built with **Flask, HTML5, CSS3, and JavaScript**. The application provides loan enquiry management, EMI calculation, secure admin authentication, and a clean user experience optimized for desktop and mobile devices.

---

## ✨ Features

- 🎯 Modern and responsive user interface
- 🔐 Secure Admin Login with BCrypt password hashing
- 📋 Loan enquiry management system
- 💰 EMI Calculator with real-time calculations
- 🛡️ Server-side validation and input sanitization
- 🚫 Rate limiting to prevent brute-force attacks
- 🍯 Honeypot spam protection
- 📦 SQLite database integration
- 📱 Mobile-friendly responsive design
- ⚡ Fast and lightweight architecture
- 🔍 SEO optimized pages with structured metadata
- ♿ Accessibility-focused UI components

---

# 📂 Project Structure

```
Tanishi Finance/
│
├── css/
│   ├── variables.css        # Global design tokens
│   ├── style.css            # Main styling
│   └── responsive.css       # Mobile responsiveness
│
├── js/
│   ├── app.js               # UI interactions
│   ├── emi.js               # EMI Calculator logic
│   ├── admin.js             # Admin panel scripts
│   └── validation.js        # Client-side validation
│
├── data/
│   └── tanishi.db           # SQLite Database
│
├── scripts/
│   ├── backup.py
│   ├── reset_admin_password.py
│   └── verify_admin_config.py
│
├── tests/
│   └── test_api.py
│
├── index.html
├── admin.html
├── app.py
├── requirements.txt
├── README.md
├── DEPLOYMENT.md
└── .env
```

---

# 🛠️ Technology Stack

### Backend

- Python 3
- Flask
- SQLite
- BCrypt
- Dotenv

### Frontend

- HTML5
- CSS3
- JavaScript (ES6)

### Security

- BCrypt Password Hashing
- HTTPOnly Cookies
- SameSite Cookies
- Rate Limiting
- Input Validation
- Honeypot Protection
- Secure Session Management

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/tanishi-finance.git
cd tanishi-finance
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy

```
.env.example
```

to

```
.env
```

Example

```env
FLASK_SECRET_KEY=your_random_secret_key

ADMIN_USERNAME=admin

ADMIN_PASSWORD_HASH=your_bcrypt_hash

COOKIE_SECURE=False
```

---

## 5. Run the Application

```bash
python app.py
```

Open

```
http://127.0.0.1:5055
```

Admin Dashboard

```
http://127.0.0.1:5055/admin.html
```

---

# 🔑 Admin Authentication

The admin dashboard uses:

- BCrypt password hashing
- Secure sessions
- HTTPOnly cookies
- Login rate limiting
- Protected API endpoints

To generate a new password hash:

```bash
python scripts/reset_admin_password.py
```

Verify configuration:

```bash
python scripts/verify_admin_config.py
```

---

# 📊 Available Utilities

Run API tests

```bash
python -m unittest tests/test_api.py
```

Create Backup

```bash
python scripts/backup.py
```

Health Check

```
http://127.0.0.1:5055/healthz
```

---

# 🔒 Security Features

✔ BCrypt Password Hashing

✔ Session Authentication

✔ Secure Cookies

✔ CSRF-aware Design

✔ Rate Limiting

✔ Input Validation

✔ Honeypot Spam Protection

✔ SQLite Data Storage

✔ Server-side Validation

✔ Production-ready Flask Configuration

---

# 🚀 Deployment

The project can be deployed free of cost on platforms such as:

- Render
- Railway
- Fly.io
- PythonAnywhere
- Koyeb

For production deployment:

- Enable HTTPS
- Set `COOKIE_SECURE=True`
- Use Gunicorn or Waitress
- Store secrets in environment variables
- Configure automated backups
- Use monitoring and logging
- Replace SQLite with PostgreSQL for high-traffic environments

Refer to **DEPLOYMENT.md** for complete deployment instructions.

---

# 📈 Future Enhancements

- Customer Login Portal
- Loan Status Tracking
- Email Notifications
- SMS OTP Verification
- Admin Analytics Dashboard
- Document Upload
- Payment Gateway Integration
- PostgreSQL Migration
- REST API
- Docker Support
- CI/CD Pipeline

---

# 📄 License

This project is intended for Personal and business demonstration purposes.

---

# 👨‍💻 Developer

**Gaurav Kumar**

AI & ML Developer

Built with ❤️ using Flask and Modern Web Technologies.
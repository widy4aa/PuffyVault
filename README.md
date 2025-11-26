# ☁️🔒 PuffyVault

> *Your cozy, cloud-like sanctuary for secrets* ✨

Where your notes float safely in end-to-end encryption heaven, and the server never peeks! 💙

[![Made with Flask](https://img.shields.io/badge/Backend-Flask%203.0-blue?logo=flask)](https://flask.palletsprojects.com/)
[![Made with PHP](https://img.shields.io/badge/Frontend-PHP%208.3-777BB4?logo=php)](https://www.php.net/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2015-336791?logo=postgresql)](https://www.postgresql.org/)
[![AES-256-GCM](https://img.shields.io/badge/Encryption-AES--256--GCM-green?logo=letsencrypt)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)

## 🌟 What is PuffyVault?

PuffyVault is a **zero-knowledge**, **end-to-end encrypted** notes app where:

- 🔐 **Your password = Your encryption key** (we never see it!)
- ☁️ **Notes encrypted in your browser** before sending to server
- 🛡️ **Server is blind** - can't read your notes even if hacked
- 💙 **Cute & minimal UI** - Shadcn-inspired design
- 🌙 **Dark mode** - Easy on the eyes
- 📱 **Mobile-friendly** - Works on all devices

**Think of it as:** A fluffy cloud ☁️ that keeps your secrets safe with military-grade encryption 🔒, but with a cute interface that doesn't make you feel like you're in a spy movie 💕

---

## ✨ Features

### 🔐 Security First
- **AES-256-GCM Encryption** - Industry standard, NSA-approved
- **PBKDF2 Key Derivation** - 100,000 iterations with SHA-256
- **Bcrypt Password Hashing** - 12 rounds for your password
- **JWT Authentication** - Stateless, secure tokens (24h expiry)
- **Zero-Knowledge** - Server never sees plaintext
- **Authentication Tags** - Detect tampering & ensure integrity

### 📝 Note Management
- ✅ Create encrypted notes
- ✅ View & decrypt notes (in browser only)
- ✅ Edit notes (re-encrypted automatically)
- ✅ Delete notes (soft/hard delete)
- ✅ Search notes (by metadata)

### 🎨 User Experience
- ✅ Cute landing page with PuffyVault branding
- ✅ Minimal, Shadcn-inspired UI
- ✅ Dark/Light mode toggle
- ✅ Mobile responsive design
- ✅ Smooth animations & transitions

---

## 🏗️ Architecture

### Zero-Knowledge Encryption Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                         │
│  (Browser - Where Magic Happens ✨)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Password  ──→  PBKDF2 (100k iterations)              │
│                      ↓                                      │
│                 AES-256 Key (32 bytes)                      │
│                      ↓                                      │
│  Plaintext Note  ──→  AES-256-GCM Encryption               │
│                      ↓                                      │
│  Ciphertext + IV + Auth Tag                                │
│       │                                                     │
└───────┼─────────────────────────────────────────────────────┘
        │
        │ HTTPS (encrypted_content, iv, auth_tag)
        ↓
┌─────────────────────────────────────────────────────────────┐
│                         SERVER SIDE                         │
│  (Flask API - Blind & Happy 🙈)                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PostgreSQL Database                                        │
│  ├─ users (email, password_hash, salt)                      │
│  ├─ notes (encrypted_content, iv, auth_tag)                 │
│  └─ jwt_blacklist (logout tokens)                           │
│                                                             │
│  ⚠️ Server NEVER sees plaintext!                            │
│  ✅ Even if hacked, data is useless without your password   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

#### Backend (Flask API)
- **Flask 3.0** - Web framework
- **PostgreSQL 15** - Database
- **SQLAlchemy** - ORM
- **PyJWT 2.8.0** - JWT authentication
- **Bcrypt 4.1.1** - Password hashing
- **Pydantic 2.5.2** - Data validation

#### Frontend (PHP MVC)
- **PHP 8.3** - Server-side language
- **Bootstrap 5.3.2** - UI framework
- **Vanilla JavaScript** - No dependencies!
- **Web Crypto API** - Client-side encryption
- **Custom CSS** - Shadcn-inspired minimal design

#### Security Layer
- **AES-256-GCM** - Symmetric encryption (client-side)
- **PBKDF2** - Key derivation (100k iterations)
- **Bcrypt** - Password hashing (12 rounds)
- **JWT HS256** - Token authentication

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** with pip
- **PHP 8.3+** with built-in server
- **PostgreSQL 15+** running locally
- **Modern browser** with Web Crypto API support

### Installation

#### 1. Clone Repository
```powershell
git clone https://github.com/widy4aa/PuffyVault.git
cd PuffyVault
```

#### 2. Setup Database
```powershell
# Create database
psql -U postgres
CREATE DATABASE nazril;
\q

# Initialize tables
python database/create_tables.py

# (Optional) Seed test data
python database/seed_data.py
```

#### 3. Setup Backend
```powershell
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run backend server
python run.py
```

Backend API running on **http://localhost:5000** 🎉

#### 4. Setup Frontend
```powershell
# Open new terminal
cd frontend/php/public

# Run PHP server
php -S localhost:8000
```

Frontend running on **http://localhost:8000** 🎉

#### 5. Open Browser
```
http://localhost:8000
```

🌈 Welcome to PuffyVault! Create an account and start securing your notes! ☁️✨

---

## 🎯 Usage

### 1️⃣ Create Account
- Click **"Create Account"** on landing page
- Enter email & strong password (min 12 chars, mixed case, numbers, symbols)
- Submit and you're registered! 🎉

### 2️⃣ Login
- Enter your email & password
- Your password is used to derive encryption key (PBKDF2)
- You receive JWT token (valid 24 hours)

### 3️⃣ Create Note
- Click **"+ New Note"**
- Write your secret note ✍️
- Click **"Save"**
- Magic happens:
  1. Browser generates random IV
  2. Encrypts note with AES-256-GCM
  3. Sends ciphertext to server
  4. Server stores encrypted blob (can't read it!)

### 4️⃣ View Note
- Click **"View"** on any note
- Browser fetches encrypted data
- Decrypts with your password-derived key
- Displays plaintext (only you can see!) 👀

### 5️⃣ Edit/Delete
- Edit: Decrypt → Modify → Re-encrypt → Save
- Delete: Soft delete (mark as deleted) or hard delete (permanent)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[BACKEND.md](docs/BACKEND.md)** | Flask API documentation, endpoints, database schema |
| **[FRONTEND.md](docs/FRONTEND.md)** | PHP MVC architecture, routing, UI components |
| **[TUTORIAL.md](docs/TUTORIAL.md)** | Step-by-step user guide for using PuffyVault |
| **[SRS.md](docs/SRS.md)** | Software Requirements Specification (detailed specs) |
| **[TESTING.md](docs/TESTING_GUIDE.md)** | API testing with Postman & cURL |

---

## 🧪 Test Accounts

Seed data includes 3 test users:

| Email | Password | Notes |
|-------|----------|-------|
| alice@example.com | AlicePass123! | 3 notes |
| bob@example.com | BobSecure456! | 2 notes |
| charlie@example.com | Charlie789!@# | 1 note |

---

## 🔐 Security Highlights

### Why PuffyVault is Secure

1. **Zero-Knowledge Architecture**
   - Server never has access to your plaintext notes
   - Even database admin can't read your data
   - Your password = your encryption key (never stored!)

2. **Military-Grade Encryption**
   - AES-256-GCM (same as Signal, WhatsApp E2EE)
   - PBKDF2 with 100,000 iterations (OWASP recommended)
   - Bcrypt password hashing with 12 rounds

3. **Authentication & Integrity**
   - JWT tokens with HS256 signing
   - Authentication tags verify data integrity
   - Token blacklist on logout

4. **No Password Recovery**
   - By design! (zero-knowledge)
   - If you forget password, notes are lost forever
   - This is a feature, not a bug! 🎯

### Security Trade-offs

⚠️ **Important Limitations:**

- ❌ **No password recovery** - Forgot password = Lost notes (by design)
- ❌ **Can't search encrypted content** - Server can't index ciphertext
- ❌ **Password change** = Old notes unreadable (unless re-encrypted)
- ❌ **Shared notes not supported** - Each user has their own encryption key

## 📁 Project Structure

```
PuffyVault/
├── backend/                    # Flask API Backend
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   ├── middleware/        # Auth & error handlers
│   │   ├── utils/             # Security utilities
│   │   └── main.py            # Flask app
│   ├── tests/                 # Unit & integration tests
│   ├── run.py                 # Server entry point
│   └── requirements.txt
│
├── frontend/                   # PHP Frontend
│   └── php/
│       ├── app/
│       │   ├── controllers/   # MVC Controllers
│       │   ├── models/        # API Client wrappers
│       │   ├── views/         # Templates
│       │   └── core/          # Router & base
│       ├── public/
│       │   ├── assets/
│       │   │   ├── css/       # Minimal.css
│       │   │   └── js/        # Encryption.js
│       │   └── index.php
│       └── config/
│
├── database/                   # Database Setup Scripts
│   ├── create_tables.py       # Create DB tables
│   ├── init_db.py             # Initialize database
│   ├── migrations.py          # SQL migrations
│   ├── seed_data.py           # Dummy data for testing
│   └── README.md
│
└── docs/                       # Documentation
    ├── srs                    # Software Requirements Spec
    ├── BACKEND_README.md      # Backend documentation
    ├── FRONTEND_README.md     # Frontend documentation
    ├── PENJELASAN_KODE.md     # Code explanation (Bahasa)
    ├── TESTING_GUIDE.md       # Testing guide
    └── Secure_Notes_API.postman_collection.json
```

## 🔒 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user baru
- `POST /api/auth/login` - Login dan dapatkan JWT token

### Notes
- `POST /api/notes` - Buat catatan baru
- `GET /api/notes` - Ambil semua catatan
- `GET /api/notes/:id` - Ambil satu catatan
- `PUT /api/notes/:id` - Update catatan
- `DELETE /api/notes/:id` - Hapus catatan

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Test dengan Postman
Import file: backend/Secure_Notes_API.postman_collection.json
```

---

## 💙 Made with Love

Built with lots of encryption math and puffy clouds ☁️🔒

**Stack:** Flask 3.0 + PHP 8.3 + PostgreSQL 15 + AES-256-GCM  
**Architecture:** Zero-Knowledge, End-to-End Encrypted  
**UI:** Minimal, Shadcn-inspired, Mobile-First  
**Security:** Military-Grade Encryption, OWASP Best Practices  

---

## 🙏 Acknowledgments

- **Flask** - Amazing Python web framework
- **Web Crypto API** - Browser-native encryption
- **Shadcn UI** - Design inspiration
- **OWASP** - Security best practices
- **NIST** - Cryptographic standards

---

<div align="center">

**[⭐ Star this repo](https://github.com/widy4aa/PuffyVault)** if you learned something! 

Made by [widy4aa](https://github.com/widy4aa) with 💙

*Keep your secrets puffy and safe!* ☁️✨🔒

</div>

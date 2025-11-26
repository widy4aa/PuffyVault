# PuffyVault

🔐 **Secure Notes Web App** - Aplikasi catatan pribadi terenkripsi dengan end-to-end encryption

## ✨ Features

- ✅ **End-to-End Encryption** - AES-256-GCM encryption di client-side
- ✅ **Zero-Knowledge Architecture** - Server tidak pernah tahu plaintext content
- ✅ **Secure Authentication** - JWT + Bcrypt password hashing
- ✅ **CRUD Operations** - Create, Read, Update, Delete notes
- ✅ **Multi-Device Sync** - Access notes dari berbagai device
- ✅ **Responsive Design** - Mobile-first UI dengan Shadcn-inspired minimal design

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask (Python 3.13)
- **Database:** PostgreSQL 15
- **Authentication:** JWT (PyJWT)
- **Encryption:** Web Crypto API (AES-256-GCM, PBKDF2)
- **Password Hashing:** Bcrypt

### Frontend
- **Framework:** PHP 8.3 (MVC Architecture)
- **UI Design:** Minimal.css (Shadcn-inspired)
- **JavaScript:** Vanilla JS + Web Crypto API
- **Icons:** Bootstrap Icons

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- PostgreSQL 15+
- PHP 8.3+
- Git

### Installation

1. **Clone repository**
```bash
git clone https://github.com/widy4aa/PuffyVault.git
cd PuffyVault
```

2. **Setup Backend**
```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install flask flask-cors flask-sqlalchemy psycopg2-binary sqlalchemy pyjwt bcrypt python-dotenv pydantic email-validator

# Setup database
python create_tables.py

# Run backend server
python run.py
```

Backend akan berjalan di **http://localhost:5000**

3. **Setup Frontend**
```bash
cd frontend/php

# Run PHP development server
php -S localhost:8000 -t public
```

Frontend akan berjalan di **http://localhost:8000**

## 📖 How It Works

### 🔐 Encryption Flow

1. **User Registration**
   - Password di-hash dengan Bcrypt (cost 12)
   - Generate random salt (16 bytes) untuk PBKDF2
   - Salt disimpan di database untuk key derivation

2. **Create Note**
   ```
   Plaintext → PBKDF2 (password + salt) → Encryption Key
   → AES-256-GCM Encrypt → Ciphertext + IV + Auth Tag
   → Send to Server (Base64 encoded)
   ```

3. **Read Note**
   ```
   Server → Return Ciphertext + IV + Auth Tag
   → PBKDF2 (password + salt) → Encryption Key
   → AES-256-GCM Decrypt → Plaintext
   ```

### 🔑 Security Features

- **Client-Side Encryption:** Semua enkripsi dilakukan di browser
- **Zero-Knowledge:** Server hanya menyimpan data terenkripsi
- **PBKDF2:** 100,000 iterasi untuk lambatkan brute force
- **Random IV:** Setiap enkripsi menggunakan IV yang berbeda
- **Authentication Tag:** GCM mode untuk detect tampering
- **JWT Token:** Expire dalam 24 jam

## 📁 Project Structure

```
PuffyVault/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   ├── models/            # Database models
│   │   ├── utils/             # Security utilities
│   │   └── main.py            # Flask app
│   ├── run.py                 # Entry point
│   └── requirements.txt
│
├── frontend/                   # PHP Frontend
│   └── php/
│       ├── app/
│       │   ├── controllers/   # MVC Controllers
│       │   ├── models/        # API Client
│       │   └── views/         # Blade-like templates
│       └── public/
│           ├── assets/
│           │   ├── css/       # Minimal.css
│           │   └── js/        # Encryption.js
│           └── index.php
│
└── srs                        # Software Requirements Specification
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

## 📝 Environment Variables

Create `.env` file in `backend/`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/nazril
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DEBUG=True
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Nazril**
- GitHub: [@widy4aa](https://github.com/widy4aa)

## 🙏 Acknowledgments

- [Shadcn UI](https://ui.shadcn.com/) - Design inspiration
- [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API) - Browser encryption
- [Flask](https://flask.palletsprojects.com/) - Backend framework

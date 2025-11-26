# Secure Notes Backend API

Backend API untuk aplikasi Secure Notes - Catatan pribadi terenkripsi dengan Python Flask.

## Fitur

- **End-to-End Encryption**: Semua catatan dienkripsi di client-side menggunakan AES-256-GCM
- **Zero-Knowledge Architecture**: Server tidak memiliki akses ke plaintext catatan
- **Secure Authentication**: JWT-based authentication dengan bcrypt password hashing
- **RESTful API**: API endpoints untuk manajemen user dan catatan
- **PBKDF2 Key Derivation**: Password dikonversi menjadi kunci enkripsi yang aman

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: PostgreSQL dengan SQLAlchemy ORM
- **Authentication**: PyJWT
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Testing**: pytest

## Struktur Proyek

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point aplikasi
│   ├── config.py            # Konfigurasi aplikasi
│   ├── models/              # Database models
│   │   ├── user.py
│   │   └── note.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   └── note.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── notes.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── note_service.py
│   ├── middleware/          # Middleware
│   │   ├── auth_middleware.py
│   │   └── error_handler.py
│   └── utils/               # Utilities
│       ├── security.py
│       └── validators.py
├── tests/                   # Unit tests
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md
```

## Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (untuk rate limiting)

### Instalasi

1. Clone repository dan masuk ke direktori backend:
```bash
cd backend
```

2. Buat virtual environment:
```bash
python -m venv venv
```

3. Aktifkan virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Copy file environment dan sesuaikan konfigurasi:
```bash
copy .env.example .env
```

6. Buat database PostgreSQL:
```sql
CREATE DATABASE secure_notes;
```

7. Jalankan migrasi database:
```bash
flask db upgrade
```

8. Jalankan aplikasi:
```bash
python app/main.py
```

API akan berjalan di `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register user baru
- `POST /api/auth/login` - Login dan dapatkan JWT token
- `POST /api/auth/logout` - Logout dan blacklist token
- `POST /api/auth/verify-token` - Verifikasi token validity

### User Management

- `GET /api/user/profile` - Dapatkan profil user (termasuk salt)
- `PUT /api/user/profile` - Update profil user
- `POST /api/user/change-password` - Ganti password

### Notes

- `POST /api/notes` - Buat catatan baru (encrypted)
- `GET /api/notes` - Dapatkan semua catatan user
- `GET /api/notes/{id}` - Dapatkan satu catatan
- `PUT /api/notes/{id}` - Update catatan
- `DELETE /api/notes/{id}` - Hapus catatan (soft delete)

## Environment Variables

Lihat file `.env.example` untuk daftar lengkap variabel environment yang diperlukan.

## Testing

Jalankan unit tests:
```bash
pytest
```

Jalankan dengan coverage:
```bash
pytest --cov=app tests/
```

## Security Features

1. **Password Hashing**: bcrypt dengan 12 rounds
2. **JWT Authentication**: Token expires dalam 24 jam
3. **PBKDF2 Key Derivation**: 100.000 iterasi dengan SHA-256
4. **AES-256-GCM Encryption**: Client-side encryption
5. **Rate Limiting**: 5 login attempts per 15 menit
6. **CORS Protection**: Hanya allow whitelisted domains
7. **HTTPS Only**: Semua komunikasi via TLS

## Development

### Code Style

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## License

Private project untuk pembelajaran.

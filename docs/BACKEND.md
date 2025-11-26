# 🔒 PuffyVault Backend - Flask API

> Where your secrets float safely in the cloud ☁️✨

## 📦 Tech Stack

- **Flask 3.0** - Modern Python web framework
- **PostgreSQL 15** - Robust relational database
- **SQLAlchemy** - Powerful ORM for database operations
- **PyJWT 2.8.0** - JSON Web Token authentication
- **Bcrypt 4.1.1** - Secure password hashing
- **Pydantic 2.5.2** - Data validation and serialization

## ✨ Architecture Overview

```
backend/
├── app/
│   ├── main.py              # Flask app initialization
│   ├── config.py            # Configuration (DB, JWT, etc.)
│   ├── database.py          # Database connection
│   │
│   ├── models/              # Database models (ORM)
│   │   ├── __init__.py
│   │   ├── user.py              # User table
│   │   ├── note.py              # Notes table
│   │   └── jwt_blacklist.py     # Token blacklist
│   │
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py              # /api/auth/* (register, login, logout)
│   │   ├── users.py             # /api/user/* (profile, change password)
│   │   └── notes.py             # /api/notes/* (CRUD operations)
│   │
│   └── middleware/          # Middleware & decorators
│       ├── __init__.py
│       └── auth_middleware.py   # @require_auth decorator
│
├── requirements.txt         # Python dependencies
├── run.py                   # Server entry point
└── .env                     # Environment variables
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- PostgreSQL 15+

### Installation

1. **Create Virtual Environment**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

3. **Configure Environment**
Create `.env` file:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/nazril
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this
FLASK_ENV=development
```

4. **Create Database**
```sql
CREATE DATABASE nazril;
```

5. **Initialize Tables**
```powershell
cd ..
python database/create_tables.py
```

6. **Seed Test Data** (Optional)
```powershell
python database/seed_data.py
```

7. **Run Server**
```powershell
cd backend
python run.py
```

🎉 API running on http://localhost:5000

## 📋 Database Schema

### `users` Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    salt BYTEA NOT NULL,              -- For PBKDF2 key derivation
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### `notes` Table
```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    encrypted_content BYTEA NOT NULL,  -- AES-256-GCM ciphertext
    iv BYTEA NOT NULL,                 -- Initialization Vector (16 bytes)
    auth_tag BYTEA NOT NULL,           -- Authentication Tag (16 bytes)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP
);
```

### `jwt_blacklist` Table
```sql
CREATE TABLE jwt_blacklist (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL,
    blacklisted_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL
);
```

## 🛣️ API Endpoints

### 🔐 Authentication (`/api/auth`)

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "salt": "base64_encoded_salt_here"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "salt": "base64_encoded_salt_here"
  }
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <token>
```

### 👤 User Management (`/api/user`)

#### Get Profile
```http
GET /api/user/profile
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "salt": "base64_encoded_salt_here",
    "created_at": "2025-11-20T10:00:00Z"
  }
}
```

#### Update Profile
```http
PUT /api/user/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe"
}
```

#### Change Password
```http
POST /api/user/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "SecurePass123!",
  "new_password": "NewSecurePass456!"
}
```

### 📝 Notes Management (`/api/notes`)

#### Create Note
```http
POST /api/notes
Authorization: Bearer <token>
Content-Type: application/json

{
  "encrypted_content": "base64_encoded_ciphertext",
  "iv": "base64_encoded_iv",
  "auth_tag": "base64_encoded_auth_tag"
}
```

#### Get All Notes
```http
GET /api/notes
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "notes": [
    {
      "id": 1,
      "encrypted_content": "base64_encoded_ciphertext",
      "iv": "base64_encoded_iv",
      "auth_tag": "base64_encoded_auth_tag",
      "created_at": "2025-11-20T10:00:00Z",
      "updated_at": "2025-11-20T10:00:00Z"
    }
  ]
}
```

#### Get Single Note
```http
GET /api/notes/{id}
Authorization: Bearer <token>
```

#### Update Note
```http
PUT /api/notes/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "encrypted_content": "new_base64_encoded_ciphertext",
  "iv": "new_base64_encoded_iv",
  "auth_tag": "new_base64_encoded_auth_tag"
}
```

#### Delete Note
```http
DELETE /api/notes/{id}
Authorization: Bearer <token>
```

## 🔒 Security Features

### Password Security
- **Bcrypt Hashing**: 12 rounds (2^12 iterations)
- **Automatic Salt**: Managed by bcrypt library
- **No Plaintext Storage**: Passwords never stored in plaintext

### Zero-Knowledge Architecture
```
Client                          Server
  |                               |
  | 1. User enters password       |
  | 2. PBKDF2 key derivation      |
  | 3. AES-256-GCM encryption     |
  |                               |
  | 4. Send encrypted data   ---> | 5. Store ENCRYPTED data
  |    {ciphertext, iv, tag}      |    (server never sees plaintext!)
  |                               |
  | 6. Retrieve encrypted <------ | 7. Return encrypted data
  | 7. Decrypt in browser         |
  |                               |
```

### JWT Authentication
- **Token Expiry**: 24 hours (86400 seconds)
- **Blacklist System**: Logout adds token to blacklist
- **HS256 Algorithm**: HMAC with SHA-256
- **Middleware Protection**: `@require_auth` decorator

### Encryption Parameters
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Length**: 32 bytes (256 bits)
- **IV Length**: 16 bytes (128 bits)
- **Auth Tag**: 16 bytes (128 bits)
- **Key Derivation**: PBKDF2 with 100,000 iterations, SHA-256

## 🧪 Test Users

Seed data includes 3 test users:

| Email | Password | Notes Count |
|-------|----------|-------------|
| alice@example.com | AlicePass123! | 3 |
| bob@example.com | BobSecure456! | 2 |
| charlie@example.com | Charlie789!@# | 1 |

## 🛠️ Development

### Code Structure

**Models** (`app/models/`)
- Define database tables using SQLAlchemy ORM
- Handle data serialization/deserialization
- Example: `User.create()`, `Note.find_by_id()`

**Routes** (`app/routes/`)
- Define API endpoints
- Validate request data with Pydantic schemas
- Return JSON responses

**Middleware** (`app/middleware/`)
- `@require_auth`: Verify JWT token before accessing protected routes
- Extract user info from token payload

### Middleware Example
```python
from app.middleware.auth_middleware import require_auth

@notes_bp.route('', methods=['GET'])
@require_auth
def get_notes(current_user):
    # current_user is injected by @require_auth decorator
    notes = Note.query.filter_by(user_id=current_user['id']).all()
    return jsonify({'notes': [n.to_dict() for n in notes]})
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET_KEY` | Secret for signing JWT tokens | Required |
| `FLASK_ENV` | Environment mode | `development` |
| `BCRYPT_LOG_ROUNDS` | Bcrypt cost factor | `12` |

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Check what's using port 5000
netstat -ano | findstr :5000

# Run on different port
flask --app app.main run --port 5001
```

### Database Connection Error
```powershell
# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# Check credentials in .env
```

### Import Errors
```powershell
# Make sure you're in backend/ directory
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 Dependencies

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
psycopg2-binary==2.9.9
PyJWT==2.8.0
bcrypt==4.1.1
pydantic==2.5.2
email-validator==2.1.0
python-dotenv==1.0.0
```

## 💙 API Philosophy

- **RESTful Design**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **JSON Everything**: All requests and responses use JSON
- **Security First**: Zero-knowledge architecture, never trust client
- **Developer Friendly**: Clear error messages, consistent structure

Made with love and lots of encryption math ☁️🔒

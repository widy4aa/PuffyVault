# 🧪 PuffyVault API - Testing Guide

> Test your puffy cloud sanctuary with Postman & cURL ☁️✨

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Database
Pastikan PostgreSQL sudah running dengan database `nazril`:
```sql
CREATE DATABASE nazril;
```

### 3. Create Tables
```bash
python create_tables.py
```

### 4. Seed Dummy Data
```bash
python seed_data.py
```

### 5. Run Server
```bash
flask --app app.main run --debug
```

Server akan running di: `http://localhost:5000`

---

## Test Users

### User 1: Alice
- **Email**: `alice@example.com`
- **Password**: `AlicePass123!`
- **Notes**: 3 catatan

### User 2: Bob
- **Email**: `bob@example.com`
- **Password**: `BobSecure456!`
- **Notes**: 2 catatan

### User 3: Charlie
- **Email**: `charlie@example.com`
- **Password**: `Charlie789!@#`
- **Notes**: 1 catatan

---

## Postman Testing

### Import Collection
1. Buka Postman
2. Import file: `Secure_Notes_API.postman_collection.json`
3. Create Environment baru dengan variable:
   - `auth_token` (akan auto-set saat login)

### Test Flow

#### 1. Health Check
```
GET http://localhost:5000/
GET http://localhost:5000/health
```

#### 2. Login
```
POST http://localhost:5000/api/auth/login
Body:
{
  "email": "alice@example.com",
  "password": "AlicePass123!"
}
```
Response akan berisi `token` yang otomatis tersimpan di environment.

#### 3. Get Profile (with salt)
```
GET http://localhost:5000/api/user/profile
Header: Authorization: Bearer {{auth_token}}
```

#### 4. Get All Notes
```
GET http://localhost:5000/api/notes
Header: Authorization: Bearer {{auth_token}}
```

#### 5. Create New Note
```
POST http://localhost:5000/api/notes
Header: Authorization: Bearer {{auth_token}}
Body:
{
  "encrypted_content": "base64_encoded_encrypted_data",
  "iv": "base64_encoded_iv",
  "auth_tag": "base64_encoded_tag"
}
```

#### 6. Update Note
```
PUT http://localhost:5000/api/notes/{note_id}
Header: Authorization: Bearer {{auth_token}}
Body:
{
  "encrypted_content": "new_encrypted_data",
  "iv": "new_iv",
  "auth_tag": "new_tag"
}
```

#### 7. Delete Note
```
DELETE http://localhost:5000/api/notes/{note_id}
Header: Authorization: Bearer {{auth_token}}
```

---

## Manual cURL Testing

### Register New User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "AlicePass123!"
  }'
```

### Get Notes (replace TOKEN)
```bash
curl -X GET http://localhost:5000/api/notes \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Expected Responses

### Successful Login
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "alice@example.com",
    "name": "Alice Johnson",
    "created_at": "2025-11-20T10:00:00"
  }
}
```

### Get All Notes
```json
{
  "success": true,
  "notes": [
    {
      "id": 1,
      "user_id": 1,
      "encrypted_content": "base64_string...",
      "iv": "base64_string...",
      "auth_tag": "base64_string...",
      "created_at": "2025-11-20T10:00:00",
      "updated_at": "2025-11-20T10:00:00",
      "is_deleted": false,
      "deleted_at": null
    }
  ]
}
```

### Error Response
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Invalid token",
  "status_code": 401
}
```

---

## Notes on Encryption

⚠️ **Important**: Dalam production:
- Encryption dilakukan di **client-side** (browser)
- Server hanya menerima data yang sudah terenkripsi
- `encrypted_content`, `iv`, dan `auth_tag` adalah base64 encoded

Dummy data yang di-seed menggunakan data simulasi terenkripsi untuk testing purposes.

---

## Troubleshooting

### Server tidak bisa start
```bash
# Check jika port 5000 sudah digunakan
netstat -ano | findstr :5000

# Atau gunakan port lain
flask --app app.main run --port 5001
```

### Database connection error
```bash
# Verify PostgreSQL running
pg_isready -h localhost -p 5432

# Check credentials di .env file
```

### Token expired
Login ulang untuk mendapatkan token baru (expires in 24 hours)

---

## Database Structure

### users table
- id (serial)
- email (unique)
- password_hash (bcrypt)
- name
- salt (untuk PBKDF2)
- created_at
- updated_at

### notes table
- id (serial)
- user_id (FK to users)
- encrypted_content (bytea)
- iv (bytea)
- auth_tag (bytea)
- created_at
- updated_at
- is_deleted
- deleted_at

### jwt_blacklist table
- id (serial)
- token
- blacklisted_at
- expires_at

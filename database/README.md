# Database Setup Scripts

Script untuk setup dan manage database PostgreSQL untuk PuffyVault.

## 📁 Files

- **`create_tables.py`** - Membuat semua tabel database
- **`init_db.py`** - Initialize database dengan schema
- **`migrations.py`** - SQL migrations untuk database schema
- **`seed_data.py`** - Insert dummy data untuk testing

## 🚀 Cara Penggunaan

### 1. Setup Database

Pastikan PostgreSQL sudah running dan database sudah dibuat:

```sql
CREATE DATABASE nazril;
```

### 2. Jalankan Create Tables

```bash
cd database
python create_tables.py
```

Output:
```
Creating database tables...
✓ All tables created successfully!

Created tables:
- users
- notes
- jwt_blacklist
```

### 3. (Optional) Seed Dummy Data

Untuk testing, bisa insert dummy data:

```bash
python seed_data.py
```

Output akan menampilkan:
- 3 dummy users dengan credentials
- Beberapa encrypted notes per user

### Test Users (dari seed_data.py):

```
Email: alice@example.com
Password: AlicePass123!

Email: bob@example.com
Password: BobSecure456!

Email: charlie@example.com
Password: Charlie789!@#
```

## 📊 Database Schema

### Table: `users`
```sql
- id (SERIAL PRIMARY KEY)
- email (VARCHAR UNIQUE)
- password_hash (VARCHAR)
- name (VARCHAR)
- salt (BYTEA)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Table: `notes`
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INTEGER FK)
- encrypted_content (BYTEA)
- iv (BYTEA)
- auth_tag (BYTEA)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- is_deleted (BOOLEAN)
- deleted_at (TIMESTAMP)
```

### Table: `jwt_blacklist`
```sql
- id (SERIAL PRIMARY KEY)
- token (VARCHAR)
- blacklisted_at (TIMESTAMP)
- expires_at (TIMESTAMP)
```

## ⚠️ Important Notes

- Semua script harus dijalankan dari folder `database/`
- Pastikan backend sudah terinstall dependencies-nya
- Script akan otomatis mencari backend di `../backend/`
- Database connection di-configure di `backend/app/config.py`

## 🔧 Configuration

Database URL bisa di-set via environment variable:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

Atau edit di `backend/app/config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:dio@localhost:5432/nazril'
```

# Penjelasan Struktur Kode Backend

## Struktur File Utama

```
backend/
├── run.py                    # File untuk menjalankan server
├── app/
│   ├── main.py              # Setup aplikasi Flask
│   ├── config.py            # Konfigurasi (database, JWT, dll)
│   ├── database.py          # Setup koneksi database
│   ├── models/              # Model database
│   │   ├── user.py          # Tabel users
│   │   └── note.py          # Tabel notes
│   └── routes/              # Endpoint API
│       ├── auth.py          # /api/auth/register & /api/auth/login
│       └── notes.py         # CRUD catatan
```

## Cara Kerja Aplikasi

### 1. **run.py** - Menjalankan Server
```python
# Jalankan server dengan: python run.py
# Server akan berjalan di http://localhost:5000
```

### 2. **app/main.py** - Setup Flask
```python
# Membuat aplikasi Flask
# Menghubungkan ke database
# Mendaftarkan routes (endpoint API)
```

### 3. **app/config.py** - Konfigurasi
```python
# DATABASE_URL: alamat PostgreSQL
# JWT_SECRET_KEY: kunci untuk token autentikasi
# BCRYPT_LOG_ROUNDS: tingkat keamanan password hash
```

### 4. **app/models/** - Database Tables

**user.py** - Tabel `users`
- `id`: ID user
- `email`: Email login
- `password_hash`: Password yang sudah di-hash (aman)
- `name`: Nama user
- `salt`: Kunci untuk enkripsi catatan

**note.py** - Tabel `notes`
- `id`: ID catatan
- `user_id`: Siapa pemilik catatan
- `encrypted_content`: Isi catatan (terenkripsi)
- `iv`: Initialization Vector (untuk dekripsi)
- `auth_tag`: Authentication Tag (untuk keamanan)

### 5. **app/routes/** - API Endpoints

**auth.py** - Autentikasi

1. **POST /api/auth/register** - Daftar user baru
   ```json
   Input: {"email": "user@mail.com", "password": "123456", "name": "User"}
   Output: {"message": "Registrasi berhasil", "user_id": 1}
   ```

2. **POST /api/auth/login** - Login
   ```json
   Input: {"email": "user@mail.com", "password": "123456"}
   Output: {"token": "jwt-token-disini", "user": {...}}
   ```

**notes.py** - CRUD Catatan

1. **POST /api/notes** - Buat catatan baru
   ```json
   Headers: Authorization: Bearer <token>
   Input: {"encrypted_content": "...", "iv": "...", "auth_tag": "..."}
   Output: {"message": "Catatan berhasil dibuat", "note_id": 1}
   ```

2. **GET /api/notes** - Ambil semua catatan
   ```json
   Headers: Authorization: Bearer <token>
   Output: {"notes": [...]}
   ```

3. **GET /api/notes/:id** - Ambil satu catatan
   ```json
   Headers: Authorization: Bearer <token>
   Output: {"id": 1, "encrypted_content": "...", ...}
   ```

4. **PUT /api/notes/:id** - Update catatan
   ```json
   Headers: Authorization: Bearer <token>
   Input: {"encrypted_content": "...", "iv": "...", "auth_tag": "..."}
   Output: {"message": "Catatan berhasil diupdate"}
   ```

5. **DELETE /api/notes/:id** - Hapus catatan
   ```json
   Headers: Authorization: Bearer <token>
   Output: {"message": "Catatan berhasil dihapus"}
   ```

## Alur Kerja

### 1. User Daftar (Register)
```
User kirim email + password
↓
Backend hash password dengan bcrypt
↓
Generate salt (kunci enkripsi)
↓
Simpan ke database
↓
Return user_id
```

### 2. User Login
```
User kirim email + password
↓
Backend cari user di database
↓
Verifikasi password (compare hash)
↓
Generate JWT token (berlaku 24 jam)
↓
Return token + data user (termasuk salt)
```

### 3. User Buat Catatan
```
Frontend enkripsi catatan dengan password user
↓
Kirim encrypted_content + iv + auth_tag ke backend
↓
Backend simpan ke database
↓
Return note_id
```

### 4. User Baca Catatan
```
Frontend minta data catatan (dengan token)
↓
Backend cek token valid
↓
Ambil catatan dari database
↓
Return encrypted_content + iv + auth_tag
↓
Frontend dekripsi dengan password user
```

## Keamanan

1. **Password**: Di-hash dengan bcrypt (tidak bisa di-decrypt)
2. **Catatan**: Dienkripsi dengan AES-256-GCM di frontend
3. **Token**: JWT untuk autentikasi (expired 24 jam)
4. **Database**: Hanya menyimpan data terenkripsi

## Cara Menjalankan

1. Aktifkan virtual environment:
   ```
   .\venv\Scripts\Activate.ps1
   ```

2. Jalankan server:
   ```
   python run.py
   ```

3. Server siap di: `http://localhost:5000`

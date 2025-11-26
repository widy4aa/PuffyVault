# 📋 Software Requirements Specification (SRS)

**Project:** PuffyVault - Secure Notes Web Application  
**Version:** 1.0  
**Date:** November 2025  
**Status:** Implementation Complete

---

## 1. PENDAHULUAN

### 1.1 Tujuan Dokumen
Dokumen ini mendefinisikan spesifikasi lengkap untuk **PuffyVault**, aplikasi web untuk membuat dan menyimpan catatan pribadi dengan enkripsi end-to-end dan arsitektur zero-knowledge.

### 1.2 Ruang Lingkup
PuffyVault adalah platform web yang memungkinkan user untuk:

- ✅ Membuat, membaca, memperbarui, dan menghapus catatan pribadi
- ✅ Menyimpan catatan dengan enkripsi AES-256-GCM
- ✅ Autentikasi dan manajemen akun user dengan JWT
- ✅ Akses multi-device dengan sinkronisasi aman
- ✅ Zero-knowledge architecture (server tidak bisa membaca catatan)

### 1.3 Definisi dan Singkatan

| Term | Definition |
|------|------------|
| **AES-GCM** | Advanced Encryption Standard dengan Galois/Counter Mode |
| **PBKDF2** | Password-Based Key Derivation Function 2 |
| **IV** | Initialization Vector (nonce untuk encryption) |
| **Salt** | Random data untuk key derivation |
| **Auth Tag** | Authentication Tag untuk verifikasi integritas |
| **End-to-End Encryption** | Enkripsi di client, server hanya menerima ciphertext |
| **Zero-Knowledge** | Server tidak memiliki akses ke plaintext data user |
| **JWT** | JSON Web Token untuk autentikasi stateless |

---

## 2. DESKRIPSI PRODUK

### 2.1 Perspektif Produk
PuffyVault adalah aplikasi web standalone yang menyediakan platform aman untuk menyimpan catatan pribadi dengan enkripsi client-side dan arsitektur zero-knowledge.

### 2.2 Fitur Utama

#### 🔐 User Authentication
- Register dengan email & password
- Login dengan JWT token (expires 24 jam)
- Logout dengan token blacklist
- Password hashing dengan bcrypt (12 rounds)

#### 📝 Note Management
- CRUD operations untuk catatan (Create, Read, Update, Delete)
- Soft delete dengan timestamp
- Search notes berdasarkan metadata

#### 🔒 Client-Side Encryption
- AES-256-GCM encryption di browser
- PBKDF2 key derivation (100,000 iterations)
- Random IV per encryption
- Authentication tag untuk integrity verification

#### 🛡️ Zero-Knowledge Architecture
- Server hanya menyimpan data terenkripsi
- Encryption/decryption hanya terjadi di browser
- Password tidak pernah dikirim ke server (hanya hash)

### 2.3 Karakteristik User

**Target Audience:**
- Individual users yang menginginkan privasi tinggi
- Professionals yang menangani data sensitif
- Privacy-conscious users
- Tech-savvy individuals (basic to intermediate)
- Usia 18+ tahun

**User Needs:**
- Penyimpanan catatan yang aman
- Akses multi-device
- UI yang sederhana dan intuitif
- Jaminan privasi (zero-knowledge)

---

## 3. KEBUTUHAN FUNGSIONAL

### 3.1 Modul User Management

#### FR-1: Registrasi User

**FR-1.1** - Form registrasi harus menyediakan field:
- Email (unique, valid format, required)
- Password (min 12 char, uppercase, lowercase, digit, special char, required)
- Confirm Password (must match, required)
- Name (optional)

**FR-1.2** - Proses registrasi:
1. Validasi input di client-side
2. Generate salt (16 bytes random)
3. Hash password dengan bcrypt (12 rounds)
4. Simpan user record di database
5. Return user data + salt (untuk encryption key derivation)

**FR-1.3** - Response:
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "salt": "base64_encoded_salt"
  }
}
```

#### FR-2: Login User

**FR-2.1** - User login dengan email dan password

**FR-2.2** - Sistem verifikasi password terhadap hash di database

**FR-2.3** - Jika berhasil:
- Generate JWT token dengan payload: `{user_id, email, exp}`
- Token expires dalam 86400 detik (24 jam)
- Return token + user data (including salt)

**FR-2.4** - Response:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "salt": "base64_encoded_salt"
  }
}
```

#### FR-3: Logout User

**FR-3.1** - User dapat logout dengan satu klik

**FR-3.2** - Token ditambahkan ke blacklist table:
- Token (text)
- Blacklisted_at (timestamp)
- Expires_at (timestamp)

**FR-3.3** - Session berakhir di client (clear localStorage)

#### FR-4: Manajemen Profil

**FR-4.1** - Get profile:
- Return user data (id, email, name, salt, created_at)
- Requires valid JWT token

**FR-4.2** - Update profile:
- User dapat mengubah name
- Email tidak bisa diubah

**FR-4.3** - Change password:
- Verifikasi old password terlebih dahulu
- Hash new password dengan bcrypt
- Update password_hash di database
- ⚠️ **Note:** Changing password will make old notes unreadable (unless re-encrypted)

### 3.2 Modul Note Management

#### FR-5: Membuat Catatan (Create)

**FR-5.1** - Form create note:
- Title (optional, max 255 char)
- Content (required, max 50,000 char)
- Tags (optional, array of strings)

**FR-5.2** - Client-side encryption process:
1. User inputs plaintext note
2. Generate random IV (16 bytes)
3. Derive key from password using PBKDF2 + salt
4. Encrypt content with AES-256-GCM
5. Get authentication tag (16 bytes)

**FR-5.3** - Request payload:
```json
{
  "encrypted_content": "base64_encoded_ciphertext",
  "iv": "base64_encoded_iv",
  "auth_tag": "base64_encoded_tag"
}
```

**FR-5.4** - Server response:
```json
{
  "success": true,
  "message": "Note created successfully",
  "note": {
    "id": 1,
    "created_at": "2025-11-26T10:00:00Z"
  }
}
```

#### FR-6: Membaca Catatan (Read)

**FR-6.1** - Get all notes:
- Return list of all user's notes
- Include: id, encrypted_content, iv, auth_tag, created_at, updated_at
- Exclude soft-deleted notes (is_deleted = true)

**FR-6.2** - Get single note by ID:
- Return note if user owns it
- Return 404 if not found
- Return 403 if note belongs to different user

**FR-6.3** - Client-side decryption:
1. Receive encrypted note from server
2. Derive key from password + salt
3. Decrypt using IV and ciphertext
4. Verify authentication tag
5. Display plaintext if valid

**FR-6.4** - Decryption failure:
- If auth tag invalid → show error
- If wrong password → decryption fails
- Never display corrupted plaintext

#### FR-7: Memperbarui Catatan (Update)

**FR-7.1** - User dapat edit existing note

**FR-7.2** - Update process:
1. Fetch encrypted note from server
2. Decrypt in browser
3. User modifies plaintext
4. Generate NEW random IV
5. Re-encrypt with AES-256-GCM
6. Send new encrypted data to server

**FR-7.3** - Request payload:
```json
{
  "encrypted_content": "new_base64_encoded_ciphertext",
  "iv": "new_base64_encoded_iv",
  "auth_tag": "new_base64_encoded_tag"
}
```

**FR-7.4** - Server updates:
- Update encrypted_content, iv, auth_tag
- Update updated_at timestamp
- Return success message

#### FR-8: Menghapus Catatan (Delete)

**FR-8.1** - User dapat delete note dengan konfirmasi

**FR-8.2** - Soft delete:
- Set is_deleted = true
- Set deleted_at timestamp
- Note tetap di database tapi tidak tampil

**FR-8.3** - Hard delete (optional):
- Permanent removal dari database
- Data tidak bisa di-recover

**FR-8.4** - Response:
```json
{
  "success": true,
  "message": "Note deleted successfully"
}
```

#### FR-9: Search Catatan

**FR-9.1** - Search berdasarkan:
- Metadata (created_at, updated_at)
- Tags (jika implemented)
- ⚠️ **Limitation:** Tidak bisa search encrypted content (ciphertext)

**FR-9.2** - Client-side search:
- User dapat decrypt semua notes di browser
- Then search plaintext locally
- Slower but preserves privacy

### 3.3 Modul Security & Encryption

#### FR-10: Key Derivation

**FR-10.1** - PBKDF2 parameters:
```javascript
{
  hash: 'SHA-256',
  iterations: 100000,
  salt: user.salt, // 16 bytes from user record
  keyLength: 32    // 256 bits
}
```

**FR-10.2** - Process:
1. User inputs password
2. Retrieve salt from user profile
3. Compute: `derived_key = PBKDF2(password, salt, 100000, SHA256, 32)`
4. Use derived_key for AES-256-GCM

#### FR-11: Enkripsi Content

**FR-11.1** - AES-256-GCM parameters:
```javascript
{
  algorithm: 'AES-GCM',
  key: derived_key,      // 32 bytes from PBKDF2
  iv: random_iv,         // 16 bytes random
  tagLength: 128         // 128 bits auth tag
}
```

**FR-11.2** - Encryption process:
1. Generate cryptographically random IV (16 bytes)
2. Encrypt plaintext with AES-256-GCM
3. Produce: ciphertext + authentication tag
4. Base64 encode for transmission

#### FR-12: Decryption & Verification

**FR-12.1** - Decryption process:
1. Base64 decode ciphertext, IV, auth tag
2. Derive key from password + salt
3. Attempt decryption with AES-256-GCM
4. Verify authentication tag
5. If valid → return plaintext
6. If invalid → reject and show error

**FR-12.2** - Error handling:
- Wrong password → decryption fails
- Tampered data → auth tag mismatch
- Corrupted ciphertext → decryption error

#### FR-13: Password Hashing

**FR-13.1** - Bcrypt configuration:
```python
{
  algorithm: 'bcrypt',
  rounds: 12  # 2^12 iterations
}
```

**FR-13.2** - Process:
1. User submits password
2. Bcrypt generates salt automatically
3. Hash = bcrypt(password, salt, rounds)
4. Store hash in database (never plaintext)

---

## 4. KEBUTUHAN NON-FUNGSIONAL

### 4.1 Performance

**NFR-1** - Response time:
- API response < 500ms untuk 95% requests
- Page load < 2 seconds
- Encryption/decryption < 200ms per note

**NFR-2** - Scalability:
- Support 1000+ concurrent users
- Database can handle 1M+ notes

### 4.2 Security

**NFR-3** - Password requirements:
- Minimum 12 characters
- At least 1 uppercase, 1 lowercase, 1 digit, 1 special char

**NFR-4** - Encryption standards:
- AES-256-GCM (NIST approved)
- PBKDF2 with 100,000 iterations (OWASP recommended)
- Bcrypt with 12 rounds

**NFR-5** - JWT security:
- HS256 algorithm
- 24-hour expiration
- Secure secret key (min 32 bytes)

**NFR-6** - HTTPS only in production

### 4.3 Usability

**NFR-7** - UI/UX:
- Mobile responsive (Bootstrap 5)
- Intuitive navigation
- Clear error messages
- Dark/light mode support

**NFR-8** - Accessibility:
- Keyboard navigation support
- Screen reader compatible
- WCAG 2.1 Level AA compliance

### 4.4 Reliability

**NFR-9** - Availability:
- 99.5% uptime in production
- Graceful error handling

**NFR-10** - Data integrity:
- Database backups daily
- Transaction rollback on errors
- Authentication tag verification

### 4.5 Maintainability

**NFR-11** - Code quality:
- Modular MVC architecture
- Clear documentation
- Consistent coding style
- Unit tests for critical functions

---

## 5. CONSTRAINTS & ASSUMPTIONS

### 5.1 Constraints

1. **No password recovery** - By design (zero-knowledge architecture)
2. **Client-side encryption only** - Server never decrypts
3. **Search limitation** - Can't search encrypted content server-side
4. **Password change impact** - Old notes unreadable unless re-encrypted

### 5.2 Assumptions

1. Users have modern browsers with Web Crypto API support
2. Users understand zero-knowledge implications
3. PostgreSQL database available
4. HTTPS in production environment

---

## 6. TEKNOLOGI STACK

### Backend
- **Framework:** Flask 3.0 (Python 3.13)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Authentication:** PyJWT 2.8.0
- **Password Hashing:** Bcrypt 4.1.1

### Frontend
- **Language:** PHP 8.3 (MVC architecture)
- **UI Framework:** Bootstrap 5.3.2
- **JavaScript:** Vanilla JS (Web Crypto API)
- **Encryption:** AES-256-GCM client-side

### Security
- **Encryption:** AES-256-GCM
- **Key Derivation:** PBKDF2 (100k iterations, SHA-256)
- **Password Hash:** Bcrypt (12 rounds)
- **Token:** JWT (HS256, 24h expiry)

---

## 7. KESIMPULAN

PuffyVault menyediakan solusi aman untuk penyimpanan catatan pribadi dengan:
- ✅ Zero-knowledge architecture
- ✅ End-to-end encryption
- ✅ User-friendly interface
- ✅ Modern security standards

**Made with love and lots of encryption math** ☁️🔒✨

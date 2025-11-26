# Secure Notes - PHP Frontend

Frontend aplikasi Secure Notes menggunakan PHP murni dengan Bootstrap 5 dan Web Crypto API untuk enkripsi client-side.

## 🚀 Teknologi

- **PHP** - Server-side scripting (native, no framework)
- **Bootstrap 5.3.2** - CSS Framework
- **Bootstrap Icons** - Icon library
- **Web Crypto API** - Client-side encryption
- **Vanilla JavaScript** - No dependencies

## 🔐 Fitur Keamanan

- **Zero-Knowledge Encryption** - Semua catatan dienkripsi di browser
- **AES-256-GCM** - Standard enkripsi industri
- **PBKDF2** - Key derivation (100,000 iterations)
- **JWT Authentication** - Token-based auth
- **Dark Mode** - Tersimpan di localStorage

## 📦 Instalasi

### Prerequisites

- PHP 7.4+ dengan built-in server atau Apache/Nginx
- Backend Flask API running di `http://localhost:5000`

### Setup

1. Masuk ke direktori frontend:
```bash
cd frontend/php
```

2. Jalankan PHP built-in server:
```bash
php -S localhost:8000
```

3. Buka browser:
```
http://localhost:8000
```

## 📁 Struktur File

```
php/
├── index.php           # Redirect ke login
├── header.php          # HTML head & Bootstrap CSS
├── footer.php          # Bootstrap JS & closing tags
├── login.php           # Login page
├── register.php        # Registration page
├── notes.php           # Notes list page
├── create-note.php     # Create note page
├── edit-note.php       # Edit note page
├── js/
│   ├── app.js          # Core utilities & API client
│   └── encryption.js   # Web Crypto API encryption service
└── README.md
```

## 🧪 Test User Credentials

Backend sudah memiliki dummy data:

| Email | Password |
|-------|----------|
| alice@example.com | AlicePass123! |
| bob@example.com | BobSecure456! |
| charlie@example.com | Charlie789!@# |

## ⚙️ Konfigurasi

### Backend API URL

Edit `js/app.js` untuk mengubah API URL:

```javascript
const API_URL = 'http://localhost:5000/api';
```

## 📱 Mobile Optimization

- **Responsive Design** - Bootstrap grid system
- **Touch-friendly** - Large button targets
- **Mobile-first** - Optimized untuk perangkat mobile
- **Responsive Navigation** - Collapsed menu pada mobile
- **Flexible Cards** - Auto-adjust layout berdasarkan screen size

## 🎨 Dark Mode

Klik tombol moon/sun di navbar untuk toggle dark mode. Preferensi tersimpan otomatis di localStorage.

## 🔄 Flow Aplikasi

1. **Register** → User membuat akun dengan email & password
2. **Login** → Password digunakan untuk derive encryption key
3. **Create Note** → Catatan dienkripsi di browser sebelum dikirim
4. **View Notes** → Catatan didekripsi di browser setelah diambil
5. **Edit Note** → Catatan didekripsi, diedit, lalu dienkripsi ulang
6. **Delete Note** → Hapus catatan dari server

## 🛠️ Development

### Menjalankan di Apache/Nginx

Untuk production, gunakan Apache atau Nginx:

**Apache `.htaccess`:**
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.php [QSA,L]
```

**Nginx config:**
```nginx
location / {
    try_files $uri $uri/ /index.php?$query_string;
}
```

## 🐛 Troubleshooting

### CORS Error

Pastikan backend Flask mengaktifkan CORS untuk `http://localhost:8000`:

```python
# app/main.py
CORS(app, origins=['http://localhost:8000'])
```

### Port sudah digunakan

Gunakan port lain:
```bash
php -S localhost:8080
```

### Backend tidak terhubung

Pastikan Flask backend running:
```bash
cd ../../backend
python app/main.py
```

## 📝 License

MIT License - Free to use for personal and commercial projects.

## 👨‍💻 Developer

Developed with ❤️ for Secure Notes Project

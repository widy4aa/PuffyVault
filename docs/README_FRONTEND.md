# Secure Notes - Frontend PHP MVC with Minimal Shadcn-inspired UI

## 🎨 Design System

Aplikasi ini menggunakan design system yang terinspirasi dari **Shadcn UI** dengan pendekatan **minimalis aesthetic** dan **mobile-first**:

- ✨ CSS Variables untuk theming (light/dark mode)
- 🎯 Clean & minimal component design
- 📱 Mobile-optimized responsive layout
- 🌈 Smooth transitions & micro-interactions
- 🔒 End-to-end encrypted notes

## 📁 Struktur Folder MVC

```
frontend/php/
├── app/
│   ├── controllers/        # Controllers (AuthController, NoteController, HomeController)
│   ├── models/            # Models (User, Note, ApiClient)
│   ├── views/             # Views (auth, notes, layouts)
│   │   ├── auth/          # Login & Register views
│   │   ├── notes/         # Notes CRUD views
│   │   └── layouts/       # Header & Footer templates
│   └── core/              # Core classes (Router, BaseController)
├── config/                # Configuration files
├── public/                # Public folder (web root)
│   ├── index.php          # Entry point
│   ├── .htaccess          # URL rewriting rules
│   └── assets/            # Static assets
│       ├── css/           # Stylesheets (minimal.css)
│       └── js/            # JavaScript files (app.js, encryption.js)
├── bootstrap.php          # Application bootstrap
└── .htaccess             # Root htaccess (redirect to public)
```

## 🚀 Cara Menjalankan

### 1. Jalankan Backend Flask (Terminal 1)
```bash
cd backend
python app.py
```

### 2. Jalankan PHP Server (Terminal 2)
```bash
cd frontend/php/public
php -S localhost:8000
```

### 3. Akses Aplikasi
Buka browser: **http://localhost:8000**

## 🎨 Design Features

### Color System
- Light mode: Clean white backgrounds dengan subtle gray accents
- Dark mode: Dark gray backgrounds dengan muted colors
- Primary color: Modern blue (#3b82f6)

### Typography
- Font: System fonts (-apple-system, Segoe UI, Roboto)
- Font weights: 500 (medium), 600 (semibold), 700 (bold)
- Letter spacing: -0.025em untuk headings

### Components

#### 1. Cards
```css
.card-minimal
- Soft shadows dengan hover effect
- Smooth transform on hover (translateY -2px)
- Border radius: 0.5rem
```

#### 2. Buttons
```css
.btn-minimal
- Multiple variants: primary, secondary, outline, ghost, destructive
- Inline-flex dengan gap 0.5rem
- Smooth transitions (0.2s cubic-bezier)
```

#### 3. Inputs
```css
.input-minimal
- Focus ring dengan primary color
- Placeholder text dengan muted color
- Auto-resize untuk textarea
```

#### 4. Navbar
```css
.navbar-minimal
- Glass morphism (backdrop-filter blur)
- Sticky positioning
- Subtle border-bottom
```

### Animations
- **slideDown**: Alert muncul dari atas
- **fadeIn**: Smooth fade untuk cards
- **fadeOut**: Smooth fade keluar
- **spin**: Loading spinner rotation

## 🔐 Security Features

1. **End-to-end Encryption**: Notes dienkripsi dengan AES-256-GCM
2. **Client-side Encryption**: Encryption dilakukan di browser
3. **Zero-knowledge**: Server tidak pernah tahu plaintext
4. **JWT Authentication**: Secure token-based auth
5. **PBKDF2 Key Derivation**: 100,000 iterations SHA-256

## 📱 Mobile Optimization

- **Touch-friendly**: Button sizing optimal untuk touch
- **Responsive grid**: 1 kolom mobile, 2 tablet, 3 desktop
- **Hidden elements**: Text disembunyikan di mobile untuk space
- **Viewport meta**: Proper scaling untuk mobile devices
- **Flexible layouts**: Flexbox & Grid untuk responsive design

## 🎯 Routes

| Route | Controller | Method | Description |
|-------|-----------|--------|-------------|
| `/` | HomeController | index | Redirect to login |
| `/login` | AuthController | showLogin | Login page |
| `/register` | AuthController | showRegister | Register page |
| `/logout` | AuthController | logout | Logout user |
| `/notes` | NoteController | index | Notes list |
| `/notes/create` | NoteController | create | Create note page |
| `/notes/:id/edit` | NoteController | edit | Edit note page |

## 🛠️ Technologies

- **Backend**: Python 3.13, Flask 3.1.2
- **Frontend**: PHP 7.4+, Vanilla JavaScript
- **Database**: PostgreSQL 15
- **Encryption**: Web Crypto API (AES-256-GCM, PBKDF2)
- **UI**: Custom CSS (Shadcn-inspired), Bootstrap Icons
- **Architecture**: MVC Pattern with Router

## 📝 Test Accounts

```
Email: alice@example.com
Password: AlicePass123!

Email: bob@example.com
Password: BobSecure456!

Email: charlie@example.com
Password: Charlie789!@#
```

## 🎨 UI Screenshots

### Light Mode
- Clean white backgrounds
- Subtle gray borders
- Modern blue accents

### Dark Mode
- Dark gray backgrounds (#1a1a1a)
- Muted text colors
- Soft blue highlights

## 📦 Dependencies

### Backend
- Flask 3.1.2
- PostgreSQL adapter
- PyJWT 2.8.0
- bcrypt 4.1.1
- Pydantic 2.5.2

### Frontend
- Bootstrap Icons 1.11.3
- Web Crypto API (built-in browser)
- No CSS framework dependencies (custom CSS)

## 🔧 Configuration

Edit `config/config.php`:
```php
define('APP_NAME', 'Secure Notes');
define('BASE_URL', 'http://localhost:8000');
define('API_BASE_URL', 'http://localhost:5000/api');
```

## 📚 Documentation

- Password harus minimal 12 karakter
- Harus mengandung: huruf besar, kecil, angka, karakter spesial
- Notes terenkripsi dengan user password
- Tidak ada password recovery (by design untuk security)

## 🎉 Features

✅ User registration & authentication
✅ Create, Read, Update, Delete notes
✅ End-to-end encryption
✅ Dark/Light mode toggle
✅ Search notes functionality
✅ Mobile responsive design
✅ Minimalist aesthetic UI
✅ Smooth animations
✅ MVC architecture
✅ RESTful API integration

## 📞 Support

Untuk pertanyaan atau bantuan, lihat dokumentasi lengkap di folder `backend/docs/`

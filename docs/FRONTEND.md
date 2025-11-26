# 🎨 PuffyVault Frontend - PHP MVC

> Your cozy, cloud-like sanctuary built with PHP ☁️✨

## 📦 Tech Stack

- **PHP 8.3+** - Pure PHP MVC (no framework dependencies)
- **Bootstrap 5.3.2** - Minimal, Shadcn-inspired UI
- **Web Crypto API** - Client-side AES-256-GCM encryption
- **Vanilla JavaScript** - Zero dependencies, pure power

## ✨ Architecture Overview

```
frontend/php/
├── app/
│   ├── controllers/          # Request handlers
│   │   ├── HomeController.php    # Landing page
│   │   ├── AuthController.php    # Login & Register
│   │   └── NoteController.php    # Notes CRUD
│   │
│   ├── models/               # API communication
│   │   ├── ApiClient.php         # Base HTTP client
│   │   ├── User.php              # User operations
│   │   └── Note.php              # Note operations
│   │
│   ├── views/                # UI templates
│   │   ├── home/
│   │   │   └── index.php         # Landing page
│   │   ├── auth/
│   │   │   ├── login.php         # Login form
│   │   │   └── register.php      # Registration form
│   │   ├── notes/
│   │   │   ├── index.php         # Notes dashboard
│   │   │   ├── create.php        # Create note
│   │   │   └── edit.php          # Edit note
│   │   └── layouts/
│   │       ├── header.php        # HTML head
│   │       └── footer.php        # Scripts & footer
│   │
│   └── core/                 # Framework core
│       ├── Router.php            # URL routing
│       └── BaseController.php    # Base controller
│
├── config/
│   └── config.php            # App configuration
│
├── public/                   # Web root
│   ├── index.php                 # Entry point
│   ├── .htaccess                 # URL rewriting
│   └── assets/
│       ├── css/
│       │   └── minimal.css       # Shadcn-inspired styles
│       └── js/
│           ├── app.js            # API client & utilities
│           └── encryption.js     # Zero-knowledge encryption
│
└── bootstrap.php             # App initialization
```

## 🚀 Quick Start

### Prerequisites
- PHP 8.3+ with built-in server
- Backend Flask API running on `localhost:5000`

### Run Development Server
```powershell
cd frontend/php/public
php -S localhost:8000
```

🌐 Open http://localhost:8000 in your browser

## 🔐 Zero-Knowledge Encryption Flow

```
User Password
    ↓
PBKDF2 (100k iterations, SHA-256)
    ↓
AES-256-GCM Key (32 bytes)
    ↓
┌─────────────────────────────────┐
│  Encrypt in Browser             │
│  - Generate random IV (16 bytes)│
│  - Encrypt note content         │
│  - Generate auth tag (16 bytes) │
└─────────────────────────────────┘
    ↓
Send to Server: {encrypted_content, iv, auth_tag}
    ↓
Server stores ENCRYPTED data (never sees plaintext!)
```

## 🎨 Design System

### Color Palette
```css
/* Light Mode */
--background: #ffffff
--foreground: #0a0a0a
--primary: #3b82f6

/* Dark Mode */
--background: #1a1a1a
--foreground: #fafafa
--primary: #60a5fa
```

### Components
- **Cards**: Soft shadows, hover transforms
- **Buttons**: 5 variants (primary, secondary, outline, ghost, destructive)
- **Inputs**: Focus rings, smooth transitions
- **Navbar**: Glass morphism with backdrop blur
- **Animations**: Smooth 200ms cubic-bezier transitions

## 🛣️ Routing

| Route | Controller | Method | Description |
|-------|-----------|--------|-------------|
| `/` | HomeController | index | Landing page |
| `/login` | AuthController | showLogin | Login form |
| `/register` | AuthController | showRegister | Registration form |
| `/logout` | AuthController | logout | Clear session |
| `/notes` | NoteController | index | Notes dashboard |
| `/notes/create` | NoteController | create | Create note form |
| `/notes/:id/edit` | NoteController | edit | Edit note form |

### Dynamic Parameters
Routes with `:id` automatically pass the ID to the controller method:
```php
// Route: /notes/123/edit
public function edit($id) {
    // $id = 123
}
```

## 📡 API Integration

### Models communicate with Flask backend:

```php
// User Model
$user = new User();
$response = $user->login($email, $password);
$profile = $user->getProfile($token);

// Note Model
$note = new Note();
$notes = $note->getAll($token);
$note->create($token, $encrypted_content, $iv, $auth_tag);
```

### ApiClient Base Class
All models extend `ApiClient` which provides:
- `get($endpoint, $token)` - GET request
- `post($endpoint, $data, $token)` - POST request
- `put($endpoint, $data, $token)` - PUT request
- `delete($endpoint, $token)` - DELETE request

## 🎯 MVC Pattern

### Controller Example
```php
class NoteController extends BaseController {
    public function index() {
        // Check authentication
        if (!isset($_SESSION['token'])) {
            $this->redirect('/login');
            return;
        }
        
        // Render view with data
        $this->view('notes/index', [
            'title' => 'My Notes'
        ]);
    }
}
```

### View Example
```php
<?php include VIEW_PATH . '/layouts/header.php'; ?>

<div class="container">
    <h1><?= htmlspecialchars($title) ?></h1>
    <!-- Content here -->
</div>

<?php include VIEW_PATH . '/layouts/footer.php'; ?>
```

## 🔒 Security Features

1. **Client-Side Encryption**: AES-256-GCM (notes never leave browser unencrypted)
2. **JWT Authentication**: Secure token-based auth
3. **PBKDF2 Key Derivation**: 100,000 iterations with SHA-256
4. **XSS Protection**: All output escaped with `htmlspecialchars()`
5. **CSRF Protection**: Session-based validation
6. **Password Validation**: Min 12 chars (upper, lower, digit, special)

## 📱 Mobile Optimization

- **Responsive Grid**: 1 column (mobile) → 2 (tablet) → 3 (desktop)
- **Touch-Friendly**: Large button targets (min 44x44px)
- **Mobile-First CSS**: Breakpoints at 640px, 768px, 1024px
- **Viewport Meta**: Proper scaling for mobile devices
- **Flexible Layouts**: Flexbox & Grid for responsive design

## 🎨 Dark Mode

Toggle dark mode with the moon/sun button in navbar. Preference saved in `localStorage`.

```javascript
// Toggle dark mode
document.body.classList.toggle('dark-mode');
localStorage.setItem('theme', isDark ? 'dark' : 'light');
```

## 🧪 Test Accounts

| Email | Password |
|-------|----------|
| alice@example.com | AlicePass123! |
| bob@example.com | BobSecure456! |
| charlie@example.com | Charlie789!@# |

## 🐛 Troubleshooting

### Server won't start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
php -S localhost:8080 -t public
```

### Backend not connecting
Ensure Flask backend is running:
```powershell
cd backend
python app.py
```

### CORS errors
Backend must allow `http://localhost:8000` in CORS settings.

## 🌟 Features

✅ Landing page with cute PuffyVault branding  
✅ User registration & authentication  
✅ Create, read, update, delete notes  
✅ End-to-end encryption  
✅ Dark/Light mode toggle  
✅ Search notes functionality  
✅ Mobile responsive design  
✅ Minimalist Shadcn-inspired UI  
✅ Smooth animations & transitions  
✅ MVC architecture  
✅ Zero external dependencies  

## 💙 Made with Love

Built with lots of encryption math and puffy clouds ☁️🔒

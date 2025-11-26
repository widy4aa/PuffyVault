# Secure Notes - PHP MVC Frontend

Frontend aplikasi Secure Notes menggunakan arsitektur **Model-View-Controller (MVC)** dengan PHP murni (tanpa framework).

## 📁 Struktur Folder

```
frontend/php/
├── app/
│   ├── controllers/          # Controllers - Business logic & request handling
│   │   ├── HomeController.php
│   │   ├── AuthController.php
│   │   └── NoteController.php
│   ├── models/               # Models - API communication
│   │   ├── ApiClient.php     # Base API client
│   │   ├── User.php          # User model (auth, profile)
│   │   └── Note.php          # Note model (CRUD operations)
│   ├── views/                # Views - UI templates
│   │   ├── layouts/
│   │   │   ├── header.php    # Header template
│   │   │   └── footer.php    # Footer template
│   │   ├── auth/
│   │   │   ├── login.php     # Login page
│   │   │   └── register.php  # Register page
│   │   └── notes/
│   │       ├── index.php     # Notes list
│   │       ├── create.php    # Create note
│   │       └── edit.php      # Edit note
│   └── core/                 # Core framework files
│       ├── Router.php        # URL routing system
│       └── BaseController.php # Base controller class
├── config/
│   └── config.php            # Application configuration
├── public/                   # Public accessible directory
│   ├── index.php             # Entry point
│   ├── .htaccess             # URL rewriting rules
│   └── assets/
│       ├── js/
│       │   ├── app.js        # Main application JS
│       │   └── encryption.js # Client-side encryption
│       └── css/
├── bootstrap.php             # Application bootstrap
└── .htaccess                 # Root htaccess
```

## 🚀 Cara Menjalankan

### 1. Menggunakan PHP Built-in Server

Jalankan dari folder `public/`:

```bash
cd c:\Users\widy4aa\Desktop\project_nazril\frontend\php\public
php -S localhost:8000
```

### 2. Menggunakan Apache/Nginx

**Apache:**
- Pastikan `mod_rewrite` enabled
- Document root: `frontend/php/public`
- File `.htaccess` sudah dikonfigurasi

**Nginx:**
```nginx
server {
    listen 80;
    server_name localhost;
    root /path/to/frontend/php/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
    }
}
```

## 🔧 Konfigurasi

Edit `config/config.php`:

```php
define('BASE_URL', 'http://localhost:8000');
define('API_BASE_URL', 'http://localhost:5000/api');
```

## 📋 Routing

Routing didefinisikan di `bootstrap.php`:

```php
// Auth routes
$router->get('/login', 'AuthController@showLogin');
$router->get('/register', 'AuthController@showRegister');
$router->get('/logout', 'AuthController@logout');

// Note routes
$router->get('/notes', 'NoteController@index');
$router->get('/notes/create', 'NoteController@create');
$router->get('/notes/:id/edit', 'NoteController@edit');
```

### Format Route:
- `$router->get($path, $callback)`
- `$router->post($path, $callback)`

**Callback format:**
- `'ControllerName@methodName'`
- Dynamic parameters: `/notes/:id/edit` → `edit($id)` method

## 🏗️ Arsitektur MVC

### **Model** (`app/models/`)

Models berkomunikasi dengan Flask backend API:

```php
// Example: User model
$user = new User();
$response = $user->login($email, $password);

// Example: Note model
$note = new Note();
$notes = $note->getAll($token);
```

**ApiClient.php:**
- Base class untuk semua models
- Menyediakan methods: `get()`, `post()`, `put()`, `delete()`
- Handle HTTP requests via cURL

**User.php:**
- `register()`, `login()`, `logout()`
- `getProfile()`, `updateProfile()`
- `changePassword()`, `deleteAccount()`

**Note.php:**
- `getAll()`, `getById()`
- `create()`, `update()`, `deleteNote()`
- `search()`

### **View** (`app/views/`)

Views adalah template PHP murni:

```php
<?php include VIEW_PATH . '/layouts/header.php'; ?>

<div class="container">
    <h1><?= $title ?></h1>
    <!-- Content here -->
</div>

<?php include VIEW_PATH . '/layouts/footer.php'; ?>
```

**Variables:**
- `BASE_URL` - Base URL aplikasi
- `VIEW_PATH` - Path ke folder views
- Data dari controller via `$this->view('path', ['key' => 'value'])`

### **Controller** (`app/controllers/`)

Controllers handle request dan response:

```php
class NoteController extends BaseController {
    public function index() {
        // Render view
        $this->view('notes/index');
    }
    
    public function edit($noteId) {
        // Pass data to view
        $this->view('notes/edit', ['noteId' => $noteId]);
    }
}
```

**BaseController methods:**
- `view($path, $data)` - Render view
- `redirect($path)` - Redirect to path
- `json($data, $code)` - Return JSON response
- `getPost($key)`, `getQuery($key)` - Get request data
- `setFlash($type, $msg)`, `getFlash()` - Flash messages

## 🔐 Keamanan

### Client-Side Encryption (Zero-Knowledge)

**Encryption Flow:**
1. User password → PBKDF2 (100k iterations) → Encryption key
2. Data → AES-256-GCM encryption → Encrypted blob
3. Server hanya menerima encrypted data (tidak bisa decrypt)

**Files:**
- `public/assets/js/encryption.js` - Web Crypto API implementation
- `public/assets/js/app.js` - API client & helpers

### Authentication

- JWT token disimpan di `localStorage`
- Password user disimpan di `localStorage` (untuk encryption key)
- Auto-redirect jika tidak authenticated

## 📦 Dependencies

**Backend:**
- Bootstrap 5.3.2 (CSS framework)
- Bootstrap Icons 1.11.3

**No Build Tools Required:**
- Pure PHP (no Composer)
- Vanilla JavaScript (no npm/webpack)
- CDN untuk CSS/Icons

## 🌐 API Endpoints

Frontend berkomunikasi dengan Flask backend (`localhost:5000`):

**Auth:**
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

**User:**
- `GET /api/user/profile` - Get profile (termasuk salt)
- `PUT /api/user/profile` - Update profile
- `PUT /api/user/change-password` - Change password

**Notes:**
- `GET /api/notes` - Get all notes
- `GET /api/notes/:id` - Get note by ID
- `POST /api/notes` - Create note
- `PUT /api/notes/:id` - Update note
- `DELETE /api/notes/:id` - Delete note

## 📱 Mobile Optimization

- **Responsive Design:** Bootstrap grid system
- **Mobile-first:** Breakpoints sm, md, lg
- **Touch-friendly:** Large buttons, adequate spacing
- **Dark mode:** Theme toggle dengan localStorage

## 🐛 Debugging

**Development mode** (`config/config.php`):
```php
define('APP_ENV', 'development');
```

**Error logs:**
- PHP errors: Check terminal/console
- JavaScript errors: Browser DevTools Console
- API errors: Network tab dalam DevTools

## 📝 Catatan Penting

1. **Server harus running dari folder `public/`**
   ```bash
   cd public
   php -S localhost:8000
   ```

2. **Backend Flask harus aktif di `localhost:5000`**

3. **Password requirements:**
   - Minimal 12 karakter
   - Harus ada huruf besar, kecil, angka, special char

4. **Note encryption format:**
   - Backend menerima: `encrypted_content`, `iv`, `auth_tag`
   - Content adalah JSON string: `{"title":"...", "content":"..."}`
   - Encrypted sekali sebagai satu blob

## 🔄 Workflow Development

1. Edit controller di `app/controllers/`
2. Edit view di `app/views/`
3. Edit model di `app/models/` (jika perlu)
4. Refresh browser (no build step!)

## 📖 Contoh Penggunaan

### Menambah Route Baru

**1. Edit `bootstrap.php`:**
```php
$router->get('/profile', 'UserController@profile');
```

**2. Buat Controller:**
```php
// app/controllers/UserController.php
class UserController extends BaseController {
    public function profile() {
        $this->view('user/profile');
    }
}
```

**3. Buat View:**
```php
// app/views/user/profile.php
<?php include VIEW_PATH . '/layouts/header.php'; ?>
<h1>User Profile</h1>
<?php include VIEW_PATH . '/layouts/footer.php'; ?>
```

---

**Frontend Structure:** MVC Architecture  
**Backend API:** Flask (Python)  
**Database:** PostgreSQL  
**Encryption:** AES-256-GCM (client-side, zero-knowledge)

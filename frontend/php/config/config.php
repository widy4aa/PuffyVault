<?php
/**
 * Configuration File
 * All application configuration settings
 */

// Application Settings
define('APP_NAME', 'Secure Notes');
define('APP_ENV', 'development'); // development or production
define('BASE_URL', 'http://localhost:8000');

// API Settings
define('API_BASE_URL', 'http://localhost:5000/api');
define('API_TIMEOUT', 30);

// Path Settings
define('ROOT_PATH', dirname(__DIR__));
define('APP_PATH', ROOT_PATH . '/app');
define('VIEW_PATH', APP_PATH . '/views');
define('CONTROLLER_PATH', APP_PATH . '/controllers');
define('MODEL_PATH', APP_PATH . '/models');
define('PUBLIC_PATH', ROOT_PATH . '/public');
define('ASSET_PATH', PUBLIC_PATH . '/assets');

// Security Settings
define('SESSION_LIFETIME', 3600 * 24); // 24 hours
define('CSRF_TOKEN_NAME', '_csrf_token');

// Encryption Settings (for client-side reference)
define('PBKDF2_ITERATIONS', 100000);
define('AES_KEY_LENGTH', 256);
define('AES_MODE', 'AES-GCM');

// Session Configuration (must be set BEFORE session_start)
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    ini_set('session.cookie_secure', 0); // Set to 1 in production with HTTPS
}

// Error Reporting
if (APP_ENV === 'development') {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Timezone
date_default_timezone_set('Asia/Jakarta');

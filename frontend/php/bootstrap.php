<?php
/**
 * Bootstrap file
 * Initializes the application
 */

// Load configuration first (includes session settings)
require_once __DIR__ . '/config/config.php';

// Start session AFTER configuration
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Load core classes
require_once APP_PATH . '/core/Router.php';
require_once APP_PATH . '/core/BaseController.php';

// Initialize router
$router = new Router();

// Define routes
$router->get('/', 'HomeController@index');

// Auth routes
$router->get('/login', 'AuthController@showLogin');
$router->get('/register', 'AuthController@showRegister');
$router->get('/logout', 'AuthController@logout');

// Note routes
$router->get('/notes', 'NoteController@index');
$router->get('/notes/create', 'NoteController@create');
$router->get('/notes/:id/edit', 'NoteController@edit');

// 404 handler
$router->notFound(function() {
    http_response_code(404);
    echo '<!DOCTYPE html>
    <html>
    <head>
        <title>404 - Not Found</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { font-size: 48px; margin: 0; }
            p { font-size: 18px; color: #666; }
            a { color: #0d6efd; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Page not found</p>
        <a href="' . BASE_URL . '">Go to Home</a>
    </body>
    </html>';
});

// Dispatch request
$router->dispatch();

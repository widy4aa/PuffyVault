<?php
/**
 * Auth Controller
 * Handles authentication (login, register, logout)
 */

require_once APP_PATH . '/core/BaseController.php';
require_once MODEL_PATH . '/User.php';

class AuthController extends BaseController {
    private $userModel;
    
    public function __construct() {
        $this->userModel = new User();
    }
    
    /**
     * Show login page
     */
    public function showLogin() {
        $this->view('auth/login');
    }
    
    /**
     * Show register page
     */
    public function showRegister() {
        $this->view('auth/register');
    }
    
    /**
     * Handle logout
     */
    public function logout() {
        // Client-side will handle the actual logout via API
        // This just clears session and redirects
        session_start();
        session_destroy();
        $this->redirect('/login');
    }
}

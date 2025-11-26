<?php
/**
 * Home Controller
 * Handles home page and dashboard
 */

require_once APP_PATH . '/core/BaseController.php';

class HomeController extends BaseController {
    
    /**
     * Show home page (redirect to login or notes)
     */
    public function index() {
        // In a real app, we'd check auth here
        // For now, just redirect to login
        $this->redirect('/login');
    }
}

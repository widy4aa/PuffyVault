<?php
/**
 * Home Controller
 * Handles home page and dashboard
 */

require_once APP_PATH . '/core/BaseController.php';

class HomeController extends BaseController {
    
    /**
     * Show home page (landing page)
     */
    public function index() {
        // Check if user is already logged in
        if (isset($_SESSION['token'])) {
            $this->redirect('/notes');
            return;
        }
        
        // Show landing page
        $this->view('home/index');
    }
}

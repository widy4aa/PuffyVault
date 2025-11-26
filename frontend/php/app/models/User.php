<?php
/**
 * User Model
 * Handles user authentication and profile operations with Flask API
 */

require_once MODEL_PATH . '/ApiClient.php';

class User extends ApiClient {
    
    /**
     * Register a new user
     */
    public function register($email, $password, $confirmPassword, $name = '') {
        return $this->post('/auth/register', [
            'email' => $email,
            'password' => $password,
            'confirm_password' => $confirmPassword,
            'name' => $name
        ]);
    }
    
    /**
     * Login user
     */
    public function login($email, $password) {
        return $this->post('/auth/login', [
            'email' => $email,
            'password' => $password
        ]);
    }
    
    /**
     * Logout user
     */
    public function logout($token) {
        return $this->post('/auth/logout', [], [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Get user profile
     */
    public function getProfile($token) {
        return $this->get('/user/profile', [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Update user profile
     */
    public function updateProfile($token, $name) {
        return $this->put('/user/profile', [
            'name' => $name
        ], [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Change password
     */
    public function changePassword($token, $currentPassword, $newPassword, $confirmPassword) {
        return $this->put('/user/change-password', [
            'current_password' => $currentPassword,
            'new_password' => $newPassword,
            'confirm_password' => $confirmPassword
        ], [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Delete account
     */
    public function deleteAccount($token) {
        return $this->delete('/user/account', [
            'Authorization: Bearer ' . $token
        ]);
    }
}

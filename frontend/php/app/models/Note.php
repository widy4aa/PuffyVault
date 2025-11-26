<?php
/**
 * Note Model
 * Handles note CRUD operations with Flask API
 */

require_once MODEL_PATH . '/ApiClient.php';

class Note extends ApiClient {
    
    /**
     * Get all notes for the user
     */
    public function getAll($token) {
        return $this->get('/notes', [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Get a single note
     */
    public function getById($token, $noteId) {
        return $this->get('/notes/' . $noteId, [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Create a new note
     */
    public function create($token, $encryptedContent, $iv, $authTag) {
        return $this->post('/notes', [
            'encrypted_content' => $encryptedContent,
            'iv' => $iv,
            'auth_tag' => $authTag
        ], [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Update a note
     */
    public function update($token, $noteId, $encryptedContent, $iv, $authTag) {
        return $this->put('/notes/' . $noteId, [
            'encrypted_content' => $encryptedContent,
            'iv' => $iv,
            'auth_tag' => $authTag
        ], [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Delete a note
     */
    public function deleteNote($token, $noteId) {
        return $this->delete('/notes/' . $noteId, [
            'Authorization: Bearer ' . $token
        ]);
    }
    
    /**
     * Search notes
     */
    public function search($token, $query) {
        return $this->get('/notes/search?q=' . urlencode($query), [
            'Authorization: Bearer ' . $token
        ]);
    }
}

<?php
/**
 * Note Controller
 * Handles note CRUD operations
 */

require_once APP_PATH . '/core/BaseController.php';
require_once MODEL_PATH . '/Note.php';

class NoteController extends BaseController {
    private $noteModel;
    
    public function __construct() {
        $this->noteModel = new Note();
    }
    
    /**
     * Show notes list
     */
    public function index() {
        $this->view('notes/index');
    }
    
    /**
     * Show create note page
     */
    public function create() {
        $this->view('notes/create');
    }
    
    /**
     * Show edit note page
     */
    public function edit($noteId) {
        $this->view('notes/edit', ['noteId' => $noteId]);
    }
}

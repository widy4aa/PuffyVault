<?php include VIEW_PATH . '/layouts/header.php'; ?>

<!-- Navbar -->
<nav class="navbar-minimal" style="padding: 1rem 0;">
    <div class="container flex items-center justify-between">
        <a href="<?= BASE_URL ?>/notes" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: hsl(var(--foreground));">
            <span style="font-size: 1.75rem;">☁️🔒</span>
            <span class="font-bold" style="font-size: 1.25rem;">PuffyVault</span>
        </a>

        <div class="flex items-center gap-2">
            <!-- Dark Mode Toggle -->
            <button onclick="toggleTheme()" class="btn-minimal btn-ghost-minimal" style="padding: 0.5rem;">
                <i id="theme-icon" class="bi bi-moon-fill"></i>
            </button>

            <!-- Logout Button -->
            <button onclick="logout()" class="btn-minimal btn-destructive-minimal">
                <i class="bi bi-box-arrow-right"></i>
                <span class="hidden-mobile">Logout</span>
            </button>
        </div>
    </div>
</nav>

<!-- Main Content -->
<div class="container py-5">
    <!-- Header -->
    <div style="margin-bottom: 2rem;">
        <div class="flex flex-col" style="gap: 1.5rem;">
            <div class="flex justify-between items-center" style="flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h1 style="font-size: 1.875rem; font-weight: 700; margin-bottom: 0.25rem; letter-spacing: -0.025em;">
                        <i class="bi bi-cloud-fill" style="margin-right: 0.5rem; color: hsl(var(--primary));"></i>
                        My Secure Notes
                    </h1>
                    <p class="text-muted text-sm" style="margin: 0;">Your thoughts, encrypted & puffy safe ☁️</p>
                </div>
                <a href="<?= BASE_URL ?>/notes/create" class="btn-minimal btn-primary-minimal">
                    <i class="bi bi-plus-lg"></i>
                    New Note
                </a>
            </div>
        </div>
    </div>

    <!-- Search Bar -->
    <div style="margin-bottom: 2rem; max-width: 400px;">
        <div style="position: relative;">
            <i class="bi bi-search" style="position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: hsl(var(--muted-foreground));"></i>
            <input type="text" class="input-minimal" id="search-input" placeholder="Search notes..." style="padding-left: 2.5rem;">
        </div>
    </div>

    <!-- Alert Container -->
    <div id="alert-container"></div>

    <!-- Loading State -->
    <div id="loading-state" class="empty-state" style="display: none;">
        <div class="spinner-minimal" style="width: 2.5rem; height: 2.5rem; margin: 0 auto;"></div>
        <p class="empty-state-text" style="margin-top: 1rem;">Loading your notes...</p>
    </div>

    <!-- Empty State -->
    <div id="empty-state" class="empty-state" style="display: none;">
        <i class="bi bi-inbox empty-state-icon"></i>
        <p class="empty-state-text">No notes found. Create your first secure note!</p>
    </div>

    <!-- Notes Grid -->
    <div id="notes-grid" class="grid-minimal"></div>
</div>

<script src="<?= BASE_URL ?>/assets/js/app.js"></script>
<script src="<?= BASE_URL ?>/assets/js/encryption.js"></script>
<script>
// Check authentication
if (!checkAuth()) {
    window.location.href = '<?= BASE_URL ?>/login';
}

let allNotes = [];

// Load notes on page load
document.addEventListener('DOMContentLoaded', loadNotes);

// Search functionality
document.getElementById('search-input').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = allNotes.filter(note => 
        note.title.toLowerCase().includes(query) || 
        note.content.toLowerCase().includes(query)
    );
    renderNotes(filtered);
});

async function loadNotes() {
    const loadingState = document.getElementById('loading-state');
    const emptyState = document.getElementById('empty-state');
    const notesGrid = document.getElementById('notes-grid');
    
    loadingState.style.display = 'block';
    emptyState.style.display = 'none';
    notesGrid.innerHTML = '';
    
    try {
        const response = await apiRequest('/notes');
        const encryptedNotes = response.notes || [];
        
        // Decrypt all notes
        const email = storage.get('email');
        const password = storage.get('password');
        
        // Get user profile for salt
        const profileResponse = await apiRequest('/user/profile');
        const salt = profileResponse.salt;
        
        allNotes = await Promise.all(encryptedNotes.map(async (note) => {
            try {
                // Decrypt combined content
                const decryptedData = await encryptionService.decrypt(
                    note.encrypted_content,
                    note.iv,
                    note.auth_tag,
                    password,
                    salt
                );
                
                // Parse JSON to get title and content
                const noteData = JSON.parse(decryptedData);
                
                return {
                    id: note.id,
                    title: noteData.title,
                    content: noteData.content,
                    created_at: note.created_at
                };
            } catch (error) {
                console.error('Failed to decrypt note:', note.id, error);
                return null;
            }
        }));
        
        // Filter out failed decryptions
        allNotes = allNotes.filter(note => note !== null);
        
        renderNotes(allNotes);
        
    } catch (error) {
        showAlert('Failed to load notes: ' + error.message, 'danger');
    } finally {
        loadingState.style.display = 'none';
    }
}

function renderNotes(notes) {
    const emptyState = document.getElementById('empty-state');
    const notesGrid = document.getElementById('notes-grid');
    
    if (notes.length === 0) {
        emptyState.style.display = 'block';
        notesGrid.innerHTML = '';
        return;
    }
    
    emptyState.style.display = 'none';
    
    notesGrid.innerHTML = notes.map((note, index) => `
        <div class="card-minimal fade-in" style="animation-delay: ${index * 0.05}s; height: 100%;">
            <div class="card-body-minimal" style="height: 100%; display: flex; flex-direction: column;">
                <h3 class="font-semibold" style="font-size: 1.125rem; margin-bottom: 0.5rem; line-height: 1.4;">${escapeHtml(note.title)}</h3>
                <p class="text-muted text-sm" style="flex: 1; margin-bottom: 1rem; line-height: 1.6;">
                    ${escapeHtml(note.content.substring(0, 120))}${note.content.length > 120 ? '...' : ''}
                </p>
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
                    <small class="text-muted text-xs" style="display: flex; align-items: center; gap: 0.25rem;">
                        <i class="bi bi-calendar3"></i>
                        ${formatDate(note.created_at)}
                    </small>
                </div>
            </div>
            <div class="card-footer-minimal">
                <div style="display: flex; gap: 0.5rem;">
                    <a href="<?= BASE_URL ?>/notes/${note.id}/edit" class="btn-minimal btn-outline-minimal" style="flex: 1; font-size: 0.875rem; padding: 0.5rem;">
                        <i class="bi bi-pencil"></i>
                        Edit
                    </a>
                    <button onclick="deleteNote(${note.id})" class="btn-minimal btn-outline-minimal" style="flex: 1; font-size: 0.875rem; padding: 0.5rem; color: hsl(var(--destructive)); border-color: hsl(var(--destructive) / 0.3);">
                        <i class="bi bi-trash"></i>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

async function deleteNote(id) {
    if (!confirm('Are you sure you want to delete this note?')) {
        return;
    }
    
    try {
        await apiRequest(`/notes/${id}`, { method: 'DELETE' });
        showAlert('Note deleted successfully', 'success');
        loadNotes();
    } catch (error) {
        showAlert('Failed to delete note: ' + error.message, 'danger');
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
</script>

<?php include VIEW_PATH . '/layouts/footer.php'; ?>

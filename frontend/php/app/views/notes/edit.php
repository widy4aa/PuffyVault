<?php 
$noteId = $noteId ?? '';
include VIEW_PATH . '/layouts/header.php'; 
?>

<!-- Navbar -->
<nav class="navbar-minimal" style="padding: 1rem 0;">
    <div class="container flex items-center justify-between">
        <a href="<?= BASE_URL ?>/notes" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: hsl(var(--foreground));">
            <i class="bi bi-shield-lock-fill" style="font-size: 1.75rem; color: hsl(var(--primary));"></i>
            <span class="font-bold" style="font-size: 1.25rem;">Secure Notes</span>
        </a>

        <div class="flex items-center gap-2">
            <button onclick="toggleTheme()" class="btn-minimal btn-ghost-minimal" style="padding: 0.5rem;">
                <i id="theme-icon" class="bi bi-moon-fill"></i>
            </button>
            <button onclick="logout()" class="btn-minimal btn-destructive-minimal">
                <i class="bi bi-box-arrow-right"></i>
                <span class="hidden-mobile">Logout</span>
            </button>
        </div>
    </div>
</nav>

<!-- Main Content -->
<div class="container py-5">
    <div style="max-width: 700px; margin: 0 auto;">
        <!-- Header -->
        <div style="margin-bottom: 2rem;">
            <a href="<?= BASE_URL ?>/notes" class="btn-minimal btn-ghost-minimal" style="margin-bottom: 1rem; padding: 0.5rem 0.75rem;">
                <i class="bi bi-arrow-left"></i>
                Back to Notes
            </a>
            <h1 style="font-size: 1.875rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.025em;">
                <i class="bi bi-pencil-square" style="margin-right: 0.5rem; color: hsl(var(--primary));"></i>
                Edit Note
            </h1>
            <p class="text-muted text-sm" style="margin: 0;">Update your encrypted note</p>
        </div>

        <!-- Loading State -->
        <div id="loading-state" class="empty-state">
            <div class="spinner-minimal" style="width: 2.5rem; height: 2.5rem; margin: 0 auto;"></div>
            <p class="empty-state-text" style="margin-top: 1rem;">Loading note...</p>
        </div>

        <!-- Form Card -->
        <div class="card-minimal" id="edit-form-container" style="display: none;">
            <div class="card-body-minimal">
                <!-- Alert Container -->
                <div id="alert-container"></div>

                <form id="edit-form">
                    <!-- Title -->
                    <div class="mb-4">
                        <label for="title" class="label-minimal">Title</label>
                        <input type="text" class="input-minimal" id="title" placeholder="Enter note title" required>
                    </div>

                    <!-- Content -->
                    <div class="mb-4">
                        <label for="content" class="label-minimal">Content</label>
                        <textarea class="input-minimal" id="content" rows="12" placeholder="Write your note content here..." required></textarea>
                    </div>

                    <!-- Buttons -->
                    <div class="flex gap-2" style="margin-top: 1.5rem;">
                        <a href="<?= BASE_URL ?>/notes" class="btn-minimal btn-outline-minimal" style="flex: 1;">
                            <i class="bi bi-x-lg"></i>
                            Cancel
                        </a>
                        <button type="submit" class="btn-minimal btn-primary-minimal" id="submit-btn" style="flex: 1;">
                            <span class="spinner-minimal" id="loading" style="display: none;"></span>
                            <i class="bi bi-check-lg" id="check-icon"></i>
                            <span id="btn-text">Update Note</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<script src="<?= BASE_URL ?>/assets/js/app.js"></script>
<script src="<?= BASE_URL ?>/assets/js/encryption.js"></script>
<script>
if (!checkAuth()) {
    window.location.href = '<?= BASE_URL ?>/login';
}

const noteId = '<?= $noteId ?>';

if (!noteId) {
    window.location.href = '<?= BASE_URL ?>/notes';
}

// Load note on page load
document.addEventListener('DOMContentLoaded', loadNote);

async function loadNote() {
    const loadingState = document.getElementById('loading-state');
    const formContainer = document.getElementById('edit-form-container');
    
    try {
        const email = storage.get('email');
        const password = storage.get('password');
        
        // Get user salt
        const profileResponse = await apiRequest('/user/profile');
        const salt = profileResponse.salt;
        
        // Get note
        const response = await apiRequest(`/notes/${noteId}`);
        const note = response.note;
        
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
        
        // Set form values
        document.getElementById('title').value = noteData.title;
        document.getElementById('content').value = noteData.content;
        
        loadingState.style.display = 'none';
        formContainer.style.display = 'block';
        
    } catch (error) {
        showAlert('✗ Failed to load note: ' + error.message, 'danger');
        setTimeout(() => {
            window.location.href = '<?= BASE_URL ?>/notes';
        }, 2000);
    }
}

document.getElementById('edit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const loading = document.getElementById('loading');
    const checkIcon = document.getElementById('check-icon');
    
    submitBtn.disabled = true;
    loading.style.display = 'inline-block';
    checkIcon.style.display = 'none';
    btnText.textContent = 'Updating...';
    
    try {
        const email = storage.get('email');
        const password = storage.get('password');
        
        // Get user salt
        const profileResponse = await apiRequest('/user/profile');
        const salt = profileResponse.salt;
        
        // Combine title and content as JSON for encryption
        const noteData = JSON.stringify({
            title: title,
            content: content
        });
        
        // Encrypt combined data
        const encrypted = await encryptionService.encrypt(noteData, password, salt);
        
        await apiRequest(`/notes/${noteId}`, {
            method: 'PUT',
            body: JSON.stringify({
                encrypted_content: encrypted.encrypted_content,
                iv: encrypted.iv,
                auth_tag: encrypted.auth_tag
            })
        });
        
        showAlert('✓ Note updated successfully!', 'success');
        
        setTimeout(() => {
            window.location.href = '<?= BASE_URL ?>/notes';
        }, 600);
        
    } catch (error) {
        showAlert('✗ Failed to update note: ' + error.message, 'danger');
        submitBtn.disabled = false;
        loading.style.display = 'none';
        checkIcon.style.display = 'inline-block';
        btnText.textContent = 'Update Note';
    }
});
</script>

<?php include VIEW_PATH . '/layouts/footer.php'; ?>

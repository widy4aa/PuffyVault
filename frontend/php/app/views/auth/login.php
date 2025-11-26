<?php include VIEW_PATH . '/layouts/header.php'; ?>

<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem 0;">
    <div class="container" style="max-width: 400px;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 2rem;" class="fade-in">
            <div style="margin-bottom: 1rem;">
                <i class="bi bi-shield-lock-fill" style="font-size: 3.5rem; background: linear-gradient(135deg, hsl(var(--primary)), hsl(var(--primary)) 80%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
            </div>
            <h1 style="font-size: 1.875rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.025em;">Welcome Back</h1>
            <p class="text-muted text-sm">Sign in to access your secure notes</p>
        </div>

        <!-- Form Card -->
        <div class="card-minimal fade-in" style="animation-delay: 0.1s;">
            <div class="card-body-minimal">
                <!-- Alert Container -->
                <div id="alert-container"></div>

                <form id="login-form">
                    <!-- Email -->
                    <div class="mb-4">
                        <label for="email" class="label-minimal">Email Address</label>
                        <input type="email" class="input-minimal" id="email" placeholder="Enter your email" required>
                    </div>

                    <!-- Password -->
                    <div class="mb-4">
                        <label for="password" class="label-minimal">Password</label>
                        <input type="password" class="input-minimal" id="password" placeholder="Enter your password" required>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="btn-minimal btn-primary-minimal w-full" id="submit-btn" style="margin-top: 1.5rem;">
                        <span class="spinner-minimal" id="loading" style="display: none;"></span>
                        <span id="btn-text">Sign In</span>
                    </button>
                </form>

                <div style="margin-top: 1.5rem; text-align: center;">
                    <p class="text-muted text-sm" style="margin: 0;">
                        Don't have an account?
                        <a href="<?= BASE_URL ?>/register" style="color: hsl(var(--primary)); text-decoration: none; font-weight: 500;">Create one</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="<?= BASE_URL ?>/assets/js/app.js"></script>
<script>
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const loading = document.getElementById('loading');
    
    // Show loading
    submitBtn.disabled = true;
    loading.style.display = 'inline-block';
    btnText.textContent = 'Signing in...';
    
    try {
        const response = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        // Store token and user data
        storage.set('token', response.token);
        storage.set('email', email);
        storage.set('password', password);
        
        showAlert('✓ Login berhasil! Mengalihkan...', 'success');
        
        setTimeout(() => {
            window.location.href = '<?= BASE_URL ?>/notes';
        }, 800);
        
    } catch (error) {
        showAlert('✗ Login gagal: ' + error.message, 'danger');
        submitBtn.disabled = false;
        loading.style.display = 'none';
        btnText.textContent = 'Sign In';
    }
});
</script>

<?php include VIEW_PATH . '/layouts/footer.php'; ?>

<?php include VIEW_PATH . '/layouts/header.php'; ?>

<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem 0;">
    <div class="container" style="max-width: 480px;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 2rem;" class="fade-in">
            <div style="margin-bottom: 1rem;">
                <i class="bi bi-person-plus-fill" style="font-size: 3.5rem; background: linear-gradient(135deg, hsl(var(--primary)), hsl(var(--primary)) 80%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
            </div>
            <h1 style="font-size: 1.875rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.025em;">Create Account</h1>
            <p class="text-muted text-sm">Sign up to start securing your notes</p>
        </div>

        <!-- Form Card -->
        <div class="card-minimal fade-in" style="animation-delay: 0.1s;">
            <div class="card-body-minimal">
                <!-- Alert Container -->
                <div id="alert-container"></div>

                <form id="register-form">
                    <!-- Email -->
                    <div class="mb-4">
                        <label for="email" class="label-minimal">Email Address</label>
                        <input type="email" class="input-minimal" id="email" placeholder="Enter your email" required>
                    </div>

                    <!-- Password -->
                    <div class="mb-4">
                        <label for="password" class="label-minimal">Password</label>
                        <input type="password" class="input-minimal" id="password" minlength="12" placeholder="Create a strong password" required>
                        <small class="text-muted text-xs" style="display: block; margin-top: 0.5rem;">
                            Minimal 12 karakter dengan huruf besar, kecil, angka, dan simbol
                        </small>
                    </div>

                    <!-- Confirm Password -->
                    <div class="mb-4">
                        <label for="confirm-password" class="label-minimal">Confirm Password</label>
                        <input type="password" class="input-minimal" id="confirm-password" placeholder="Confirm your password" required>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="btn-minimal btn-primary-minimal w-full" id="submit-btn" style="margin-top: 1.5rem;">
                        <span class="spinner-minimal" id="loading" style="display: none;"></span>
                        <span id="btn-text">Create Account</span>
                    </button>
                </form>

                <div style="margin-top: 1.5rem; text-align: center;">
                    <p class="text-muted text-sm" style="margin: 0;">
                        Already have an account?
                        <a href="<?= BASE_URL ?>/login" style="color: hsl(var(--primary)); text-decoration: none; font-weight: 500;">Sign in</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="<?= BASE_URL ?>/assets/js/app.js"></script>
<script>
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const loading = document.getElementById('loading');
    
    // Validate password
    if (password.length < 12) {
        showAlert('✗ Password minimal 12 karakter', 'danger');
        return;
    }
    
    // Check password complexity
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    if (!hasUpperCase) {
        showAlert('✗ Password harus mengandung huruf besar', 'danger');
        return;
    }
    if (!hasLowerCase) {
        showAlert('✗ Password harus mengandung huruf kecil', 'danger');
        return;
    }
    if (!hasNumber) {
        showAlert('✗ Password harus mengandung angka', 'danger');
        return;
    }
    if (!hasSpecial) {
        showAlert('✗ Password harus mengandung karakter spesial', 'danger');
        return;
    }
    
    if (password !== confirmPassword) {
        showAlert('✗ Password tidak sama', 'danger');
        return;
    }
    
    // Show loading
    submitBtn.disabled = true;
    loading.style.display = 'inline-block';
    btnText.textContent = 'Creating account...';
    
    try {
        await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ 
                email, 
                password,
                confirm_password: confirmPassword,
                name: null
            })
        });
        
        showAlert('✓ Akun berhasil dibuat! Mengalihkan ke login...', 'success');
        
        setTimeout(() => {
            window.location.href = '<?= BASE_URL ?>/login';
        }, 1200);
        
    } catch (error) {
        let errorMsg = 'Gagal membuat akun';
        const errorText = error.message.toLowerCase();
        
        if (errorText.includes('409') || errorText.includes('exists') || errorText.includes('already')) {
            errorMsg = 'Email sudah terdaftar';
        } else if (errorText.includes('password')) {
            errorMsg = 'Password tidak memenuhi syarat';
        } else if (errorText.includes('email')) {
            errorMsg = 'Format email tidak valid';
        }
        
        showAlert('✗ ' + errorMsg, 'danger');
        submitBtn.disabled = false;
        loading.style.display = 'none';
        btnText.textContent = 'Create Account';
    }
});
</script>

<?php include VIEW_PATH . '/layouts/footer.php'; ?>

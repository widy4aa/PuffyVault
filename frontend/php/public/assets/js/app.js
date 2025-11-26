const API_URL = 'http://localhost:5000/api';

// Storage helpers
const storage = {
    set: (key, value) => localStorage.setItem(key, value),
    get: (key) => localStorage.getItem(key),
    remove: (key) => localStorage.removeItem(key),
    clear: () => localStorage.clear()
};

// Theme management
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-bs-theme') || 'light';
    const newTheme = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    storage.set('theme', newTheme);
    updateThemeIcon();
}

function updateThemeIcon() {
    const theme = document.documentElement.getAttribute('data-bs-theme');
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }
}

// API helpers
async function apiRequest(endpoint, options = {}) {
    const token = storage.get('token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Show alert message
function showAlert(message, type = 'success') {
    const alertDiv = document.getElementById('alert-container');
    if (!alertDiv) return;
    
    const alertHtml = `
        <div class="alert-minimal alert-${type}" style="animation: slideDown 0.3s ease;">
            ${message}
        </div>
    `;
    
    alertDiv.innerHTML = alertHtml;
    
    // Auto dismiss after 4 seconds
    setTimeout(() => {
        const alert = alertDiv.querySelector('.alert-minimal');
        if (alert) {
            alert.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }
    }, 4000);
}

// Logout
function logout() {
    storage.clear();
    window.location.href = 'login.php';
}

// Check authentication
function checkAuth() {
    const token = storage.get('token');
    if (!token) {
        window.location.href = 'login.php';
        return false;
    }
    return true;
}

// Initialize theme icon on load
document.addEventListener('DOMContentLoaded', () => {
    updateThemeIcon();
});

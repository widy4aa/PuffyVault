<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 PuffyVault - Your Secure Notes Sanctuary</title>
    <link rel="stylesheet" href="<?= BASE_URL ?>/assets/css/minimal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        .hero-section {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, hsl(var(--card)) 0%, hsl(var(--background)) 100%);
            padding: 2rem 1rem;
        }
        
        .logo-puffy {
            font-size: 5rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
        
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, hsl(var(--primary)), hsl(220, 90%, 65%));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -0.05em;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: hsl(var(--muted-foreground));
            margin-bottom: 2.5rem;
            max-width: 500px;
            line-height: 1.6;
        }
        
        .feature-card {
            background: hsl(var(--card));
            border: 1px solid hsl(var(--border));
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -10px hsl(var(--primary) / 0.2);
            border-color: hsl(var(--primary));
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.75rem;
            display: block;
        }
        
        .cta-buttons {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .btn-hero {
            padding: 1rem 2.5rem;
            font-size: 1.125rem;
            font-weight: 600;
            border-radius: 0.75rem;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-hero-primary {
            background: hsl(var(--primary));
            color: white;
            border: 2px solid hsl(var(--primary));
        }
        
        .btn-hero-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px -6px hsl(var(--primary) / 0.5);
        }
        
        .btn-hero-secondary {
            background: transparent;
            color: hsl(var(--foreground));
            border: 2px solid hsl(var(--border));
        }
        
        .btn-hero-secondary:hover {
            background: hsl(var(--card));
            border-color: hsl(var(--primary));
        }
        
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2rem;
            }
            
            .logo-puffy {
                font-size: 3.5rem;
            }
            
            .cta-buttons {
                flex-direction: column;
                width: 100%;
            }
            
            .btn-hero {
                width: 100%;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="hero-section">
        <div class="container" style="max-width: 900px; text-align: center;">
            <!-- Logo & Title -->
            <div class="fade-in">
                <div class="logo-puffy">☁️🔒</div>
                <h1 class="hero-title">PuffyVault</h1>
                <p class="hero-subtitle" style="margin-left: auto; margin-right: auto;">
                    Your cozy, cloud-like sanctuary for secrets ✨<br>
                    Where notes float safely in end-to-end encryption heaven
                </p>
            </div>
            
            <!-- CTA Buttons -->
            <div class="cta-buttons fade-in" style="animation-delay: 0.2s;">
                <a href="<?= BASE_URL ?>/login" class="btn-hero btn-hero-primary">
                    <i class="bi bi-box-arrow-in-right"></i> Sign In
                </a>
                <a href="<?= BASE_URL ?>/register" class="btn-hero btn-hero-secondary">
                    <i class="bi bi-person-plus"></i> Create Account
                </a>
            </div>
            
            <!-- Features Grid -->
            <div style="margin-top: 4rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
                <div class="feature-card fade-in" style="animation-delay: 0.3s;">
                    <span class="feature-icon">🛡️</span>
                    <h3 style="font-weight: 600; margin-bottom: 0.5rem; font-size: 1.125rem;">Zero-Knowledge</h3>
                    <p class="text-muted text-sm" style="margin: 0;">Only you can decrypt your notes. We never see your secrets!</p>
                </div>
                
                <div class="feature-card fade-in" style="animation-delay: 0.4s;">
                    <span class="feature-icon">✨</span>
                    <h3 style="font-weight: 600; margin-bottom: 0.5rem; font-size: 1.125rem;">Puffy Simple</h3>
                    <p class="text-muted text-sm" style="margin: 0;">Clean, minimal, and cute interface. No clutter, just notes!</p>
                </div>
                
                <div class="feature-card fade-in" style="animation-delay: 0.5s;">
                    <span class="feature-icon">🔐</span>
                    <h3 style="font-weight: 600; margin-bottom: 0.5rem; font-size: 1.125rem;">Military Grade</h3>
                    <p class="text-muted text-sm" style="margin: 0;">AES-256-GCM encryption. Like a fluffy fortress for your thoughts!</p>
                </div>
            </div>
            
            <!-- Fun Note -->
            <div style="margin-top: 3rem;" class="fade-in" style="animation-delay: 0.6s;">
                <p class="text-muted text-sm">
                    <i class="bi bi-heart-fill" style="color: hsl(var(--primary));"></i>
                    Made with love and lots of encryption math
                </p>
            </div>
        </div>
    </div>
</body>
</html>

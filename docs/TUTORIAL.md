# 🎓 PuffyVault Tutorial - Step by Step Guide

> Learn how to use your cozy cloud sanctuary ☁️✨

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Your Account](#creating-your-account)
3. [Logging In](#logging-in)
4. [Creating Your First Note](#creating-your-first-note)
5. [Viewing & Searching Notes](#viewing-searching-notes)
6. [Editing Notes](#editing-notes)
7. [Deleting Notes](#deleting-notes)
8. [Understanding Encryption](#understanding-encryption)
9. [Security Best Practices](#security-best-practices)

---

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure:
- ✅ Backend server is running on `http://localhost:5000`
- ✅ Frontend server is running on `http://localhost:8000`
- ✅ Database is set up and seeded

### Accessing PuffyVault

Open your browser and go to:
```
http://localhost:8000
```

You'll see the landing page with two options:
- **Sign In** - For existing users
- **Create Account** - For new users

---

## 👤 Creating Your Account

### Step 1: Click "Create Account"

Click the **"Create Account"** button on the landing page.

### Step 2: Fill Registration Form

Enter your details:

**Email:**
```
yourname@example.com
```
✅ Must be a valid email format  
✅ Must be unique (not already registered)

**Name:**
```
Your Name
```
✅ Optional but recommended  
✅ Helps personalize your experience

**Password:**
```
MySecure@Pass2025
```

⚠️ **Password Requirements:**
- ✅ Minimum 12 characters
- ✅ At least 1 uppercase letter (A-Z)
- ✅ At least 1 lowercase letter (a-z)
- ✅ At least 1 number (0-9)
- ✅ At least 1 special character (!@#$%^&*)

**Confirm Password:**
```
MySecure@Pass2025
```
✅ Must match password exactly

### Step 3: Submit Registration

Click **"Create Account"** button.

**Success!** You'll see:
- ✅ "Registration successful!" message
- ✅ Automatic redirect to login page

---

## 🔐 Logging In

### Step 1: Enter Credentials

On the login page, enter:

**Email:**
```
yourname@example.com
```

**Password:**
```
MySecure@Pass2025
```

### Step 2: Click "Sign In"

Click the **"Sign In"** button.

**Success!** You'll be redirected to your notes dashboard.

### What Happens Behind the Scenes? 🧙‍♂️

1. Your password is used to derive an encryption key (PBKDF2)
2. Server verifies your credentials
3. You receive a JWT token (valid for 24 hours)
4. Token stored in browser for subsequent requests
5. Your encryption key stays in browser (never sent to server!)

---

## 📝 Creating Your First Note

### Step 1: Navigate to Dashboard

After login, you're on the notes dashboard. Click **"+ New Note"** button.

### Step 2: Write Your Note

**Title:**
```
My First Secure Note
```

**Content:**
```
This is my first encrypted note in PuffyVault!
Everything I write here is encrypted with AES-256-GCM.
The server never sees my plaintext content. 🔒
```

### Step 3: Save Note

Click **"Save Note"** button.

### What Happens Behind the Scenes? 🔐

```
Your Note (plaintext)
    ↓
Browser generates random IV (16 bytes)
    ↓
Encrypt with AES-256-GCM using your password-derived key
    ↓
Generate authentication tag
    ↓
Send {encrypted_content, iv, auth_tag} to server
    ↓
Server stores ENCRYPTED data (can't read it!)
    ↓
Success! Note saved securely ✨
```

**Success!** You'll see:
- ✅ "Note saved successfully!" message
- ✅ Redirect to notes list
- ✅ Your new note appears (encrypted)

---

## 🔍 Viewing & Searching Notes

### Viewing All Notes

On the dashboard, you'll see all your notes in a card grid:

```
┌─────────────────────────────┐
│ My First Secure Note        │
│ Created: Nov 26, 2025       │
│ [View] [Edit] [Delete]      │
└─────────────────────────────┘
```

### Viewing Single Note

Click **"View"** button on any note card.

**What you'll see:**
- 📄 Decrypted title
- 📝 Decrypted content
- 🕒 Creation timestamp
- 🕒 Last updated timestamp

### Search Functionality

Use the search bar at the top:

```
🔍 Search notes...
```

**Search works on:**
- ✅ Note titles (if stored as plaintext)
- ✅ Tags/categories
- ⚠️ NOT on encrypted content (can't search ciphertext!)

---

## ✏️ Editing Notes

### Step 1: Open Edit Mode

From notes list, click **"Edit"** button on the note you want to modify.

### Step 2: Modify Content

**Original:**
```
This is my first encrypted note in PuffyVault!
```

**Updated:**
```
This is my first encrypted note in PuffyVault!

Update: I just learned how to edit notes! 🎉
The old content is decrypted, I edit it, then it's
re-encrypted with a NEW random IV before saving.
```

### Step 3: Save Changes

Click **"Update Note"** button.

**What Happens Behind the Scenes? 🔄**

```
1. Fetch encrypted note from server
2. Decrypt with your key (in browser)
3. Display plaintext in editor
4. You make changes
5. Generate NEW random IV
6. Encrypt updated content with AES-256-GCM
7. Send NEW encrypted data to server
8. Old encrypted version is replaced
```

**Success!** Note updated with new encrypted content.

---

## 🗑️ Deleting Notes

### Step 1: Click Delete

From notes list, click **"Delete"** button.

### Step 2: Confirm Deletion

A confirmation dialog appears:

```
⚠️ Delete this note?
This action cannot be undone!

[Cancel] [Delete]
```

Click **"Delete"** to confirm.

**What Happens:**
- Note is soft-deleted (marked `is_deleted = true`)
- Or hard-deleted (permanently removed from database)
- No longer appears in your notes list

**Success!** Note deleted permanently.

---

## 🔐 Understanding Encryption

### Zero-Knowledge Architecture

```
┌──────────────┐         ┌──────────────┐
│   Browser    │         │    Server    │
│  (You see)   │         │ (Never sees) │
└──────────────┘         └──────────────┘
       │                        │
  Your Password              JWT Token
       │                        │
  PBKDF2 Key ────────X──────    │
  (100k iter)        │          │
       │             │          │
  Plaintext Note     │     Encrypted Note
       │             │          │
  AES-256-GCM ───────┼──────────┤
  Encryption         │          │
       │             │          │
  Ciphertext ────────┼─────────►│
  + IV + Auth Tag    │    Store in DB
       │             │          │
       ▼             X          ▼
  Decryption    (Can't decrypt!)
```

### Key Points

1. **Your password = Your encryption key**
   - Password never stored in plaintext
   - Used to derive AES key via PBKDF2

2. **Server is blind**
   - Server only sees encrypted blobs
   - Can't read your notes even if hacked

3. **Each encryption is unique**
   - Random IV generated every time
   - Same note encrypted twice = different ciphertext

4. **Authentication tag ensures integrity**
   - Detects tampering
   - If data modified, decryption fails

---

## 🛡️ Security Best Practices

### ✅ DO's

**Strong Password:**
```
Good: MySuper$ecureP@ss2025!
Bad:  password123
```

**Unique Passwords:**
- Don't reuse passwords from other sites
- Use password manager if needed

**Regular Logouts:**
- Click logout when done
- Especially on shared computers

**HTTPS in Production:**
- Always use HTTPS in production
- Prevents man-in-the-middle attacks

### ❌ DON'Ts

**Don't Share Password:**
- Never share password via email/chat
- No one (including admins) needs it

**Don't Use Public Computers:**
- Avoid untrusted devices
- Your key stays in browser memory

**Don't Forget Password:**
- ⚠️ **NO PASSWORD RECOVERY!**
- If you forget password, notes are LOST FOREVER
- This is by design (zero-knowledge)

**Don't Use Weak Passwords:**
```
❌ password
❌ 123456
❌ qwerty
❌ Password1
```

---

## 🎯 Quick Tips

### Tip 1: Remember Your Password! 🔑
There's NO password recovery. Write it down somewhere safe if needed.

### Tip 2: Logout After Use 🚪
Especially on shared computers. Token expires after 24 hours anyway.

### Tip 3: Use Strong Passwords 💪
Minimum 12 characters with mixed case, numbers, and symbols.

### Tip 4: Regular Backups 💾
Export/backup important notes (if feature available).

### Tip 5: Check HTTPS 🔒
In production, ensure URL starts with `https://`.

---

## 🆘 Troubleshooting

### Problem: Can't Login

**Possible Causes:**
- ❌ Wrong email or password
- ❌ Account doesn't exist
- ❌ Backend server down

**Solution:**
1. Verify email spelling
2. Check password (case-sensitive!)
3. Try registering if account doesn't exist
4. Check if backend is running

### Problem: Can't Decrypt Note

**Possible Causes:**
- ❌ Wrong password
- ❌ Data corrupted
- ❌ Authentication tag mismatch

**Solution:**
- Password must be EXACT same as when encrypted
- If data corrupted, note is lost (sorry!)

### Problem: Session Expired

**Message:** "Token expired, please login again"

**Solution:**
- JWT token expires after 24 hours
- Simply login again to get new token

---

## 🎉 You're All Set!

You've learned:
- ✅ How to create an account
- ✅ How to login securely
- ✅ How to create encrypted notes
- ✅ How to edit and delete notes
- ✅ How zero-knowledge encryption works
- ✅ Security best practices

Enjoy your puffy, secure cloud sanctuary! ☁️🔒✨

---

## 📞 Need Help?

- 📖 Read [SRS.md](./SRS.md) for detailed specifications
- 🔧 Read [BACKEND.md](./BACKEND.md) for API details
- 🎨 Read [FRONTEND.md](./FRONTEND.md) for frontend architecture
- 🧪 Read [TESTING.md](./TESTING.md) for API testing

**Made with love and lots of encryption math** 💙

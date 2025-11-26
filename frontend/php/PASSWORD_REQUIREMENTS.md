# Contoh Password Valid untuk Registrasi

Aplikasi ini memerlukan password dengan keamanan tinggi:

## Syarat Password:
✅ Minimal 12 karakter
✅ Minimal 1 huruf besar (A-Z)
✅ Minimal 1 huruf kecil (a-z)  
✅ Minimal 1 angka (0-9)
✅ Minimal 1 karakter spesial (!@#$%^&*(),.?":{}|<>)

## Contoh Password Valid:

1. `SecurePass123!` ✅
2. `MyP@ssw0rd2024` ✅
3. `Strong#Pass99` ✅
4. `Test@Account1` ✅
5. `Admin!2024Pass` ✅

## Contoh Password Tidak Valid:

❌ `password` - Terlalu pendek, tidak ada huruf besar, angka, atau spesial char
❌ `Password123` - Tidak ada karakter spesial
❌ `password123!` - Tidak ada huruf besar
❌ `PASSWORD123!` - Tidak ada huruf kecil
❌ `Pass123!` - Kurang dari 12 karakter

## Test Accounts Backend:

Jika ingin langsung login tanpa register, gunakan akun dummy:

| Email | Password |
|-------|----------|
| alice@example.com | AlicePass123! |
| bob@example.com | BobSecure456! |
| charlie@example.com | Charlie789!@# |

## Troubleshooting:

**Error: "Password tidak memenuhi syarat keamanan"**
- Pastikan password Anda memenuhi SEMUA syarat di atas
- Cek ada huruf besar DAN kecil
- Pastikan ada minimal 1 angka
- Pastikan ada minimal 1 karakter spesial seperti !@#$%^&*

**Error: "Email sudah terdaftar"**
- Email sudah digunakan, gunakan email lain
- Atau login dengan email tersebut

**Error: "Data tidak valid"**
- Periksa format email (harus valid seperti user@example.com)
- Pastikan password dan confirm password sama persis

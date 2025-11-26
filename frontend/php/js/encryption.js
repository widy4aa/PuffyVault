class EncryptionService {
    constructor() {
        this.algorithm = 'AES-GCM';
        this.keyLength = 256;
        this.ivLength = 12;
        this.tagLength = 16;
        this.iterations = 100000;
    }

    // Generate random bytes
    generateRandomBytes(length) {
        return crypto.getRandomValues(new Uint8Array(length));
    }

    // String to ArrayBuffer
    str2ab(str) {
        const encoder = new TextEncoder();
        return encoder.encode(str);
    }

    // ArrayBuffer to String
    ab2str(buffer) {
        const decoder = new TextDecoder();
        return decoder.decode(buffer);
    }

    // ArrayBuffer to Base64
    ab2base64(buffer) {
        const bytes = new Uint8Array(buffer);
        let binary = '';
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    }

    // Base64 to ArrayBuffer
    base642ab(base64) {
        const binary = atob(base64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return bytes.buffer;
    }

    // Derive key from password using PBKDF2
    async deriveKey(password, salt) {
        const passwordBuffer = this.str2ab(password);
        const saltBuffer = this.str2ab(salt);

        const importedKey = await crypto.subtle.importKey(
            'raw',
            passwordBuffer,
            'PBKDF2',
            false,
            ['deriveBits', 'deriveKey']
        );

        return await crypto.subtle.deriveKey(
            {
                name: 'PBKDF2',
                salt: saltBuffer,
                iterations: this.iterations,
                hash: 'SHA-256'
            },
            importedKey,
            {
                name: this.algorithm,
                length: this.keyLength
            },
            false,
            ['encrypt', 'decrypt']
        );
    }

    // Encrypt plaintext
    async encrypt(plaintext, password, salt) {
        try {
            const key = await this.deriveKey(password, salt);
            const iv = this.generateRandomBytes(this.ivLength);
            const plaintextBuffer = this.str2ab(plaintext);

            const ciphertext = await crypto.subtle.encrypt(
                {
                    name: this.algorithm,
                    iv: iv,
                    tagLength: this.tagLength * 8
                },
                key,
                plaintextBuffer
            );

            // Split ciphertext and auth tag
            const ciphertextArray = new Uint8Array(ciphertext);
            const encryptedContent = ciphertextArray.slice(0, ciphertextArray.length - this.tagLength);
            const authTag = ciphertextArray.slice(ciphertextArray.length - this.tagLength);

            return {
                encrypted_content: this.ab2base64(encryptedContent),
                iv: this.ab2base64(iv),
                auth_tag: this.ab2base64(authTag)
            };
        } catch (error) {
            console.error('Encryption error:', error);
            throw new Error('Failed to encrypt data');
        }
    }

    // Decrypt ciphertext
    async decrypt(encryptedContent, iv, authTag, password, salt) {
        try {
            const key = await this.deriveKey(password, salt);
            const ivBuffer = this.base642ab(iv);
            const encryptedBuffer = this.base642ab(encryptedContent);
            const authTagBuffer = this.base642ab(authTag);

            // Combine encrypted content and auth tag
            const ciphertext = new Uint8Array(
                encryptedBuffer.byteLength + authTagBuffer.byteLength
            );
            ciphertext.set(new Uint8Array(encryptedBuffer), 0);
            ciphertext.set(new Uint8Array(authTagBuffer), encryptedBuffer.byteLength);

            const decryptedBuffer = await crypto.subtle.decrypt(
                {
                    name: this.algorithm,
                    iv: new Uint8Array(ivBuffer),
                    tagLength: this.tagLength * 8
                },
                key,
                ciphertext
            );

            return this.ab2str(decryptedBuffer);
        } catch (error) {
            console.error('Decryption error:', error);
            throw new Error('Failed to decrypt data');
        }
    }
}

const encryptionService = new EncryptionService();

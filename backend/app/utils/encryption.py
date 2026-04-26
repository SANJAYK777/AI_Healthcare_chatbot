"""
AES-256 Encryption Module
Provides secure encryption/decryption for sensitive healthcare data
"""
import base64
from cryptography.fernet import Fernet
import os


class EncryptionService:
    """Handles AES-256 encryption/decryption using Fernet"""
    
    def __init__(self, encryption_key: str):
        """
        Initialize encryption service
        Args:
            encryption_key: 32-byte base encryption key
        """
        # Derive a Fernet-compatible key from the provided key
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()
        
        # Pad or trim to 32 bytes
        if len(encryption_key) < 32:
            encryption_key = encryption_key.ljust(32, b'\0')
        else:
            encryption_key = encryption_key[:32]
        
        # Create a proper Fernet key
        self.key = base64.urlsafe_b64encode(encryption_key)
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt data using AES-256
        Args:
            data: Plain text to encrypt
        Returns:
            Encrypted data as base64 string
        """
        try:
            if isinstance(data, str):
                data = data.encode()
            encrypted = self.cipher.encrypt(data)
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt data using AES-256
        Args:
            encrypted_data: Encrypted data as base64 string
        Returns:
            Decrypted plain text
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")


def get_encryption_service(encryption_key: str) -> EncryptionService:
    """Get an instance of EncryptionService"""
    return EncryptionService(encryption_key)

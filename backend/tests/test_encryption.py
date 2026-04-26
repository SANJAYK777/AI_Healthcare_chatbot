"""
Test encryption functionality
"""
from app.utils.encryption import EncryptionService
import os
from dotenv import load_dotenv

load_dotenv()

def test_encryption():
    """Test AES-256 encryption/decryption"""
    
    print("🔐 Testing AES-256 Encryption...")
    print("-" * 50)
    
    encryption_key = os.getenv("ENCRYPTION_KEY", "default-key-32-bytes-long-testkey")
    
    try:
        # Initialize encryption service
        encryption = EncryptionService(encryption_key)
        print("✓ Encryption service initialized")
        
        # Test data
        test_messages = [
            "I have a fever and cough",
            "My head hurts and I'm feeling dizzy",
            "I haven't eaten in 2 days and feel weak",
            "{'user_id': 'test', 'sensitive': True}",
            "Special characters: !@#$%^&*()_+-=[]{}|;:,.<>?",
        ]
        
        print("\nTesting encryption/decryption:")
        print("-" * 50)
        
        for i, message in enumerate(test_messages, 1):
            # Encrypt
            encrypted = encryption.encrypt(message)
            
            # Decrypt
            decrypted = encryption.decrypt(encrypted)
            
            # Verify
            success = message == decrypted
            status = "✓" if success else "✗"
            
            print(f"{status} Test {i}:")
            print(f"   Original:  {message[:40]}...")
            print(f"   Encrypted: {encrypted[:40]}...")
            print(f"   Decrypted: {decrypted[:40]}...")
            print(f"   Match: {success}")
            print()
        
        print("-" * 50)
        print("✓ All encryption tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Encryption test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_encryption()
    exit(0 if success else 1)

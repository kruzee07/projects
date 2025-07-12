import hashlib
import os

def hash_with_salt(password):
    # Generate a random salt
    salt = os.urandom(16)
    
    # Combine the salt with the password
    salted_password = salt + password.encode()
    
    # Hash the salted password using SHA-256
    hash_value = hashlib.sha256(salted_password).hexdigest()
    
    print(f"Salt: {salt.hex()}")
    print(f"Salted SHA-256 Hash: {hash_value}")

# User input
user_password = input("Enter a password to hash with salt: ")
hash_with_salt(user_password)

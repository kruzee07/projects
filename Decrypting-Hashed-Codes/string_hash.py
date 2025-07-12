import hashlib

def hash_string(input_string):
    # MD5 Hash
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    print(f"MD5 Hash: {md5_hash}")
    
    # SHA-1 Hash
    sha1_hash = hashlib.sha1(input_string.encode()).hexdigest()
    print(f"SHA-1 Hash: {sha1_hash}")
    
    # SHA-256 Hash
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
    print(f"SHA-256 Hash: {sha256_hash}")

# User input
user_input = input("Enter a string to hash: ")
hash_string(user_input)

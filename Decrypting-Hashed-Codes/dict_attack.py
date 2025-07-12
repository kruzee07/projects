import hashlib

def crack_hash(hash_to_crack, hash_type, dictionary_file):
    try:
        with open(dictionary_file, 'r') as f:
            for line in f:
                password = line.strip()
                # Create the hash based on the selected hash type
                if hash_type == "md5":
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "sha1":
                    hashed_password = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "sha256":
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                else:
                    print("Unsupported hash type")
                    return
                
                # Check if the generated hash matches the hash to crack
                if hashed_password == hash_to_crack:
                    print(f"Password found: {password}")
                    return
        print("Password not found in dictionary.")
    except FileNotFoundError:
        print("Dictionary file not found.")

# Example usage
hash_to_crack = input("Enter the hash to crack: ")
hash_type = input("Enter hash type (md5/sha1/sha256): ")
dictionary_file = 'dictionary.txt'  # Dictionary file with common passwords
crack_hash(hash_to_crack, hash_type, dictionary_file)

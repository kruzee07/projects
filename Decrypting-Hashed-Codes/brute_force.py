import hashlib
import itertools
import string

def brute_force_md5(target_hash, max_length=5):
    characters = string.ascii_lowercase  # Brute force on lowercase letters
    for length in range(1, max_length + 1):
        for guess in itertools.product(characters, repeat=length):
            guess_str = ''.join(guess)
            guess_hash = hashlib.md5(guess_str.encode()).hexdigest()
            if guess_hash == target_hash:
                print(f"Password found: {guess_str}")
                return
    print("Password not found in given length range.")

# Example usage
hash_to_crack = input("Enter MD5 hash to brute force: ")
brute_force_md5(hash_to_crack)

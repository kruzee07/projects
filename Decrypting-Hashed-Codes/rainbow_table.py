import hashlib

def generate_rainbow_table(dictionary_file, output_file='rainbow_table.txt'):
    with open(dictionary_file, 'r') as f, open(output_file, 'w') as rf:
        for line in f:
            password = line.strip()
            md5_hash = hashlib.md5(password.encode()).hexdigest()
            rf.write(f"{password}:{md5_hash}\n")
    print(f"Rainbow table saved to {output_file}")

# Example usage
dictionary_file = 'dictionary.txt'  # Dictionary of common passwords
generate_rainbow_table(dictionary_file)

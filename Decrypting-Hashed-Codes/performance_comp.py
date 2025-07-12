import hashlib
import time

def benchmark_hashing(input_string):
    # MD5 timing
    start_time = time.time()
    hashlib.md5(input_string.encode()).hexdigest()
    print(f"MD5 Hashing Time: {time.time() - start_time} seconds")
    
    # SHA-1 timing
    start_time = time.time()
    hashlib.sha1(input_string.encode()).hexdigest()
    print(f"SHA-1 Hashing Time: {time.time() - start_time} seconds")
    
    # SHA-256 timing
    start_time = time.time()
    hashlib.sha256(input_string.encode()).hexdigest()
    print(f"SHA-256 Hashing Time: {time.time() - start_time} seconds")

# Test input
test_input = "This is a sample string to hash." * 1000  # Long input string
benchmark_hashing(test_input)

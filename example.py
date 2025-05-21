#!/usr/bin/env python3
"""
CryptoStrings Examples
----------------------
This script demonstrates the key features of the CryptoStrings library
with practical examples and output formatting.

Run this file to see a real output for almost every unique type of secure random generation we offer.
"""

import time
from CryptoStrings.core import (
    generate_bytes,
    generate_string,
    generate_number,
    generate_password,
    generate_api_key
)

def print_section(title):
    """Print a formatted section title"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")

def print_example(description, value):
    """Print an example with description and value"""
    print(f"\n{description}:")
    print(f"  {value}")

def measure_time(func, *args, **kwargs):
    """Measure execution time of a function"""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, (end - start) * 1000  # time in milliseconds

def run_examples():
    """Run all examples"""
    
    print_section("BASIC STRING GENERATION")
    
    # Hex strings
    hex_16 = generate_string(16, charset='hex')
    print_example("16-character hex string", hex_16)
    
    hex_32 = generate_string(32, charset='hex')
    print_example("32-character hex string (128 bits)", hex_32)
    
    # Base64 strings
    b64_32 = generate_string(32, charset='base64')
    print_example("32-character Base64 string", b64_32)
    
    # URL-safe strings
    url_safe = generate_string(32, charset='url_safe')
    print_example("32-character URL-safe string", url_safe)
    
    # Alphanumeric
    alnum = generate_string(16, charset='alphanumeric')
    print_example("16-character alphanumeric string", alnum)
    
    # ASCII letters only
    letters = generate_string(12, charset='ascii')
    print_example("12-character letters-only string", letters)
    
    # Digits only
    digits = generate_string(10, charset='digits')
    print_example("10-digit number string", digits)
    
    # Custom charset
    custom = generate_string(8, charset='custom', custom_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    print_example("8-character custom charset string (no similar-looking chars)", custom)
    
    print_section("BYTE GENERATION")
    
    # Raw bytes
    raw_bytes_16 = generate_bytes(16)
    print_example("16 random bytes (hex representation)", raw_bytes_16.hex())
    
    # Security levels
    bytes_medium, time_medium = measure_time(generate_bytes, 32, security_level='medium')
    bytes_high, time_high = measure_time(generate_bytes, 32, security_level='high')
    bytes_paranoid, time_paranoid = measure_time(generate_bytes, 32, security_level='paranoid')
    
    print("\nSecurity level comparison (32 bytes):")
    print(f"  Medium:   {bytes_medium.hex()[:16]}... ({time_medium:.2f}ms)")
    print(f"  High:     {bytes_high.hex()[:16]}... ({time_high:.2f}ms)")
    print(f"  Paranoid: {bytes_paranoid.hex()[:16]}... ({time_paranoid:.2f}ms)")
    
    print_section("NUMBER GENERATION")
    
    # 16-bit number
    num_16 = generate_number(16)
    print_example("16-bit random number (0-65535)", num_16)
    
    # 32-bit number
    num_32 = generate_number(32)
    print_example("32-bit random number", num_32)
    
    # 64-bit number
    num_64 = generate_number(64)
    print_example("64-bit random number", num_64)
    
    # 128-bit number
    num_128 = generate_number(128)
    print_example("128-bit random number", num_128)
    
    print_section("PASSWORD GENERATION")
    
    # Default password
    default_pass = generate_password()
    print_example("Default password (16 chars, 1+ digit, 1+ special)", default_pass)
    
    # Stronger password
    strong_pass = generate_password(length=20, min_digits=3, min_special=3)
    print_example("Strong password (20 chars, 3+ digits, 3+ special)", strong_pass)
    
    print_section("API KEY GENERATION")
    
    # Simple API key
    api_key = generate_api_key(length=24)
    print_example("API key (24 chars)", api_key)
    
    # API key with prefix
    user_api_key = generate_api_key(prefix="user_42", length=16)
    print_example("User API key with prefix", user_api_key)
    
    # Service API key
    service_api_key = generate_api_key(prefix="svc", length=32, security_level='paranoid')
    print_example("Service API key (paranoid security)", service_api_key)
    
    print_section("COMMON USE CASES")
    
    # Session token
    session = generate_string(64, charset='url_safe')
    print_example("Session token", session)
    
    # Database ID
    db_id = generate_string(24, charset='hex')
    print_example("Database record ID", db_id)
    
    # Verification code
    verify_code = generate_string(6, charset='digits')
    print_example("Email verification code", verify_code)
    
    # UUID-like identifier
    uuid_like = f"{generate_string(8, 'hex')}-{generate_string(4, 'hex')}-{generate_string(4, 'hex')}-{generate_string(4, 'hex')}-{generate_string(12, 'hex')}"
    print_example("UUID-like identifier", uuid_like)
    
    print_section("PERFORMANCE TEST")
    
    # More accurate performance test
    def time_security_level(security_level, iterations=100):
        # Warmup to initialize any static resources
        for _ in range(5):
            generate_string(32, charset='url_safe', security_level=security_level)
        
        # Actual timing
        times = []
        for _ in range(iterations):
            start = time.perf_counter()  # More precise timer
            generate_string(32, charset='url_safe', security_level=security_level)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        
        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        return avg_time, min_time, max_time
    
    iterations = 1000
    print(f"\nGenerating {iterations} tokens (32 chars) with different security levels:")
    
    print("\nSecurity level: Medium")
    avg_medium, min_medium, max_medium = time_security_level('medium', iterations)
    print(f"  Average: {avg_medium:.3f}ms per token")
    print(f"  Range:   {min_medium:.3f}ms - {max_medium:.3f}ms")
    
    print("\nSecurity level: High (default)")
    avg_high, min_high, max_high = time_security_level('high', iterations)
    print(f"  Average: {avg_high:.3f}ms per token")
    print(f"  Range:   {min_high:.3f}ms - {max_high:.3f}ms")
    
    print("\nSecurity level: Paranoid")
    avg_paranoid, min_paranoid, max_paranoid = time_security_level('paranoid', iterations)
    print(f"  Average: {avg_paranoid:.3f}ms per token")
    print(f"  Range:   {min_paranoid:.3f}ms - {max_paranoid:.3f}ms")
    
    # Summary comparison
    print("\nPerformance summary (relative to medium):")
    print(f"  Medium:   1.0x (baseline)")
    print(f"  High:     {avg_high/avg_medium:.1f}x slower")
    print(f"  Paranoid: {avg_paranoid/avg_medium:.1f}x slower")
    
    print("\nNote: Actual performance may vary by system and load.")

if __name__ == "__main__":
    run_examples()
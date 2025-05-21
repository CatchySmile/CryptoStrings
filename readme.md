# CryptoStrings

A production-ready, cryptographically secure random generator for strings, numbers, and bytes with performance optimization for high-throughput applications.

## Features

- **Security-First Design**: Generate secure random bytes with configurable security levels (`medium`, `high`, `paranoid`)
- **Multiple Output Formats**: Generate strings, numbers, API keys, passwords, and raw bytes
- **Performance Optimized**: Uses an entropy pool for efficient generation of multiple values
- **Cross-Platform Compatibility**: Works reliably across Windows, macOS, and Linux
- **Comprehensive Character Sets**: Supports hex, base64, URL-safe, alphanumeric, and custom charsets
- **Production Ready**: Input validation, error handling, and fallbacks for enterprise applications

## Installation

Install from PyPI:

```sh
pip install CryptoStrings
```

## Example usage

Refer to `example.py`. Simply run with CryptoStrings installed and watch the magic!


## Basic Usage

```python
from CryptoStrings.core import generate_bytes, generate_string, generate_number

# Generate 32 secure random bytes
random_bytes = generate_bytes(32)

# Generate a 16-character secure hex string
random_hex = generate_string(16, charset='hex')

# Generate a secure 128-bit random number
random_number = generate_number(128)
```

## Security Levels

All functions accept a `security_level` parameter:

- **medium**: Fast generation using an entropy pool (good for most applications)
- **high**: More entropy sources combined for stronger security (default)
- **paranoid**: Multiple rounds of hashing and maximum entropy gathering (slower but most secure)

```python
# Generate high-security token
token = generate_string(32, charset='base64', security_level='high')

# Generate paranoid-level key for critical applications
critical_key = generate_bytes(64, security_level='paranoid')
```

## Core Functions

### Generating Bytes

```python
from CryptoStrings.core import generate_bytes

# Generate 32 bytes (256 bits) of secure random data
key_bytes = generate_bytes(32)

# Generate with paranoid security for cryptographic keys
crypto_key = generate_bytes(32, security_level='paranoid')
```

### Generating Strings

```python
from CryptoStrings.core import generate_string

# Hexadecimal string (for IDs, hashes)
hex_id = generate_string(32, charset='hex')

# Base64 string (efficient encoding, good for tokens)
token = generate_string(64, charset='base64')

# URL-safe string (perfect for URLs, no special chars)
url_token = generate_string(32, charset='url_safe')

# Alphanumeric only (letters and numbers)
alnum = generate_string(16, charset='alphanumeric')

# ASCII letters only (A-Z, a-z)
letters = generate_string(12, charset='ascii')

# Digits only (0-9)
digits = generate_string(10, charset='digits')

# Printable ASCII (includes special characters)
complex = generate_string(20, charset='printable')

# Custom character set
custom = generate_string(16, charset='custom', custom_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
```

### Generating Numbers

```python
from CryptoStrings.core import generate_number

# Generate 32-bit number (range: 0 to 2^32-1)
num32 = generate_number(32)

# Generate 64-bit number
num64 = generate_number(64)

# Generate 128-bit number (very large integer)
num128 = generate_number(128)
```

## Advanced Functions

### Password Generation

Generate strong passwords with configurable requirements:

```python
from CryptoStrings.core import generate_password

# Generate password with default settings (16 chars, 1 digit, 1 special)
password = generate_password()

# Generate longer password with more requirements
strong_pass = generate_password(length=20, min_digits=3, min_special=3)
```

### API Key Generation

Generate API keys with optional prefixes:

```python
from CryptoStrings.core import generate_api_key

# Simple API key
api_key = generate_api_key(length=32)

# API key with prefix (format: "prefix.random_string")
user_api_key = generate_api_key(prefix="user_123", length=32)
```

## Common Use Cases

### Authentication Tokens

```python
from CryptoStrings.core import generate_string

# Session token (URL-safe for cookies/headers)
session_token = generate_string(64, charset='url_safe')

# JWT secret
jwt_secret = generate_string(32, charset='base64')
```

### Cryptographic Keys

```python
from CryptoStrings.core import generate_bytes
import base64

# Generate AES-256 key
aes_key = generate_bytes(32, security_level='paranoid')

# Format for storage/transmission
b64_key = base64.b64encode(aes_key).decode('ascii')
```

### Unique Identifiers

```python
from CryptoStrings.core import generate_string

# Database record ID
record_id = generate_string(16, charset='hex')

# Short unique code (useful for URL shorteners, confirmation codes)
short_code = generate_string(8, charset='custom', 
                           custom_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
```

## Performance Considerations

CryptoStrings uses an internal entropy pool for improved performance when generating multiple values, especially useful in high-throughput web applications.

For maximum performance with acceptable security:

```python
from CryptoStrings.core import generate_string

# Medium security is fastest while still being cryptographically secure
tokens = [generate_string(32, charset='url_safe', security_level='medium') 
          for _ in range(1000)]
```

## Cross-Platform Notes

CryptoStrings automatically adapts to the platform it's running on:

- On Unix-like systems (Linux, macOS), it can access `/dev/urandom`
- On Windows, it uses the Windows Cryptographic API when available
- Fallbacks ensure it works even when certain entropy sources are unavailable

## Thread Safety

All functions are thread-safe and can be called concurrently from multiple threads.

## Comparison with Other Libraries

```
|-----------------------------|-----------------|---------|-------|--------|
| Feature                     |  CryptoStrings  | Secrets |  UUID | Random |
|-----------------------------|-----------------|---------|-------|--------|
| Cryptographically secure    | ✅             | ✅      | ❌   | ❌     |
| Multiple security levels    | ✅             | ❌      | ❌   | ❌     |
| Performance optimization    | ✅             | ❌      | ❌   | ✅     |
| Password generation         | ✅             | 🤔      | ❌   | ❌     |
| API key generation          | ✅             | 🤔      | ❌   | ❌     |
| Custom character sets       | ✅             | ❌      | ❌   | 🤔     |
```

## License

GPL-3.0 License

---

Author: Sammy Folkhome  
Email: support@vincio.cc
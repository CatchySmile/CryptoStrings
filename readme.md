# RSNumberGen

Cryptographically secure random generator for strings, numbers, and bytes & hex.

## Features

- Generate secure random bytes with configurable security levels.
- Generate secure random strings in various charsets (`hex`, `base64`, `alphanumeric`, `printable`, `ascii`, `digits`).
- Generate secure random numbers with a specified number of bits.

## Installation

```sh
pip install RSNumberGen
```

Or, for local development:

```sh
pip install .
```

## Usage

```python
from RSNumberGen import generate_secure_bytes, generate_secure_string, generate_secure_number

# Generate 32 secure random bytes
random_bytes = generate_secure_bytes(32)

# Generate a 16-character secure hex string
random_hex = generate_secure_string(16, charset='hex')

# Generate a 64-character secure base64 string
random_b64 = generate_secure_string(64, charset='base64')

# Generate a secure 128-bit random number
random_number = generate_secure_number(128)
```

## API

### `generate_secure_bytes(length, security_level='high')`

Generates cryptographically secure random bytes.

- `length`: Number of bytes to generate.
- `security_level`: One of `'medium'`, `'high'`, or `'paranoid'`. Higher levels use more entropy sources.

### `generate_secure_string(length, charset='hex', security_level='high')`

Generates a secure random string.

- `length`: Length of the string.
- `charset`: One of `'hex'`, `'base64'`, `'alphanumeric'`, `'printable'`, `'ascii'`, `'digits'`.
- `security_level`: Passed to `generate_secure_bytes`.

### `generate_secure_number(bits, security_level='high')`

Generates a secure random integer with the specified number of bits.

- `bits`: Number of bits.
- `security_level`: Passed to `generate_secure_bytes`.

## Example

```python
from RSNumberGen import (
    generate_secure_string,
    generate_secure_number,
    generate_secure_bytes
)

print("\n🔐 SECURE STRING EXAMPLES\n" + "-"*40)
print("Base64 Token (64 chars):")
print(generate_secure_string(64, charset='base64'))
print("\nHex Token (32 chars):")
print(generate_secure_string(32, charset='hex'))
print("\nAlphanumeric Password (20 chars):")
print(generate_secure_string(20, charset='alphanumeric'))
print("\nPrintable ASCII (50 chars):")
print(generate_secure_string(50, charset='printable'))
print("\nLetters Only (A-Z, a-z, 30 chars):")
print(generate_secure_string(30, charset='ascii'))
print("\nDigits Only (10 digits):")
print(generate_secure_string(10, charset='digits'))

print("\n🔢 SECURE NUMBER EXAMPLES\n" + "-"*40)
print("128-bit secure number:")
print(generate_secure_number(128))
print("\n256-bit secure number:")
print(generate_secure_number(256))
print("\n12-bit secure number:")
print(generate_secure_number(12))

print("\n📦 SECURE BYTES EXAMPLES\n" + "-"*40)
print("128-bit key (16 bytes, hex):")
print(generate_secure_bytes(16).hex())
print("\n256-bit key (32 bytes, hex):")
print(generate_secure_bytes(32).hex())
print("\n64 bytes (raw output):")
raw_bytes = generate_secure_bytes(64)
print(f"Raw length: {len(raw_bytes)}")
print(raw_bytes)
```

## License

MIT License

---

Author: Sammy Folkhome  
Email: support@vincio.cc
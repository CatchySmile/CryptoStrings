# RSNumberGen

Cryptographically secure random generator for strings, numbers, and bytes & hex.

## Features

- Generate secure random bytes with configurable security levels.
- Generate secure random strings in various charsets (hex, base64, alphanumeric, printable, ascii, digits).
- Generate secure random numbers with a specified number of bits.

## Installation

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

# Generate a 12-character secure base64 string
random_b64 = generate_secure_string(12, charset='base64')

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

## License

MIT License

---

Author: Sammy Folkhome  
Email: support@vincio.cc

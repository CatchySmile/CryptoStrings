# secure_generator/core.py
import secrets
import string
import os
import hashlib
import base64
from datetime import datetime

def generate_bytes(length, security_level='high'):
    seed_values = []
    base_random = secrets.token_bytes(length * 2)
    seed_values.append(base_random)

    if security_level in ('medium', 'high', 'paranoid'):
        try:
            system_random = os.urandom(length)
            seed_values.append(system_random)
        except Exception:
            pass

        timestamp = str(datetime.now().timestamp()).encode()
        seed_values.append(timestamp)

    if security_level in ('high', 'paranoid'):
        try:
            with open('/dev/random', 'rb') as f:
                hw_random = f.read(min(length, 64))
                seed_values.append(hw_random)
        except Exception:
            pass

    if security_level == 'paranoid':
        process_info = str(os.getpid()).encode()
        seed_values.append(process_info)
        mixed = b''.join(seed_values)
        for _ in range(3):
            mixed = hashlib.sha512(mixed).digest()
        final_entropy = secrets.token_bytes(64)
        combined = mixed + final_entropy
        return hashlib.sha512(combined).digest()[:length]

    combined = b''.join(seed_values)
    return hashlib.sha512(combined).digest()[:length]


def generate_string(length, charset='hex', security_level='high'):
    if charset == 'hex':
        return generate_bytes((length + 1) // 2, security_level).hex()[:length]
    elif charset == 'base64':
        b64 = base64.b64encode(generate_bytes((length * 3 + 3) // 4, security_level)).decode('ascii')
        return b64[:length]
    elif charset == 'alphanumeric':
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    elif charset == 'printable':
        chars = string.printable.strip()
        return ''.join(secrets.choice(chars) for _ in range(length))
    elif charset == 'ascii':
        chars = string.ascii_letters
        return ''.join(secrets.choice(chars) for _ in range(length))
    elif charset == 'digits':
        return ''.join(str(b % 10) for b in generate_bytes(length, security_level))
    else:
        raise ValueError(f"Unknown charset: {charset}")


def generate_number(bits, security_level='high'):
    bytes_needed = (bits + 7) // 8
    value = int.from_bytes(generate_bytes(bytes_needed, security_level), byteorder='big')
    max_value = (1 << bits) - 1
    return value & max_value

# CryptoStrings/core.py
import secrets
import string
import os
import hashlib
import base64
import time
import platform
import threading
import ctypes
from datetime import datetime

# Maintain a secure entropy pool for performance optimization
class EntropyPool:
    def __init__(self, pool_size=256, refresh_interval=300):
        """Initialize entropy pool with specified size and refresh interval (seconds)"""
        self.pool_size = pool_size
        self.refresh_interval = refresh_interval
        self.pool = bytearray(secrets.token_bytes(pool_size))
        self.pool_lock = threading.Lock()
        self.last_refresh = time.time()
        self.position = 0

    def get_bytes(self, length):
        """Get bytes from the pool, refreshing if necessary"""
        with self.pool_lock:
            current_time = time.time()
            
            # Refresh if it's been too long or if we need more bytes than are available
            if (current_time - self.last_refresh > self.refresh_interval or 
                self.position + length > self.pool_size):
                self._refresh_pool()
            
            # If requested length is larger than pool, just generate directly
            if length > self.pool_size:
                return secrets.token_bytes(length)
            
            # Extract bytes from pool
            result = bytes(self.pool[self.position:self.position + length])
            self.position += length
            
            # If we've used too much, mix in additional entropy
            if self.position > self.pool_size * 0.75:
                self._refresh_pool()
                
            return result
    
    def _refresh_pool(self):
        """Refresh the entropy pool with new random data"""
        # Create new bytes using secrets module
        new_bytes = secrets.token_bytes(self.pool_size)
        
        # Mix with existing pool using XOR
        for i in range(self.pool_size):
            self.pool[i] ^= new_bytes[i]
            
        # Add entropy from other sources
        try:
            os_entropy = os.urandom(64)
            for i in range(min(64, self.pool_size)):
                self.pool[(i * 7) % self.pool_size] ^= os_entropy[i % len(os_entropy)]
        except Exception:
            pass
            
        # Reset position and update refresh time
        self.position = 0
        self.last_refresh = time.time()


# Create a singleton entropy pool
_entropy_pool = EntropyPool()


def _get_platform_entropy(length):
    """Get platform-specific entropy to complement cryptographic RNG"""
    entropy_sources = []
    
    # 1. Get basic platform info as string
    sys_info = f"{platform.platform()}-{platform.processor()}-{os.getpid()}".encode()
    entropy_sources.append(hashlib.sha256(sys_info).digest())
    
    # 2. Try OS-specific sources
    if platform.system() == "Windows":
        try:
            # Try to get performance counter on Windows
            counter = ctypes.c_ulonglong()
            ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(counter))
            entropy_sources.append(counter.value.to_bytes(8, byteorder='little'))
        except Exception:
            pass
    else:
        # Unix-like systems
        try:
            # Try /dev/urandom as fallback for non-blocking operation
            with open('/dev/urandom', 'rb') as f:
                entropy_sources.append(f.read(min(length, 64)))
        except Exception:
            pass
    
    # 3. Add timestamp with microseconds
    timestamp = str(datetime.now().timestamp()).encode()
    entropy_sources.append(timestamp)
    
    # Combine all sources
    combined = b''.join(entropy_sources)
    return hashlib.sha256(combined).digest()[:length]


def generate_bytes(length, security_level='high'):
    """
    Generate cryptographically secure random bytes
    
    Args:
        length: Number of bytes to generate
        security_level: 'medium', 'high', or 'paranoid'
        
    Returns:
        Secure random bytes of specified length
    """
    if length <= 0:
        raise ValueError("Length must be positive")
        
    # For small requests in medium security, use entropy pool for performance
    if length <= 64 and security_level == 'medium':
        return _entropy_pool.get_bytes(length)
    
    # For other cases, combine multiple entropy sources
    seed_values = []
    
    # 1. Base randomness from secrets module
    base_random = secrets.token_bytes(length)
    seed_values.append(base_random)
    
    # 2. OS randomness
    try:
        system_random = os.urandom(length)
        seed_values.append(system_random)
    except Exception:
        # Fallback to using more from secrets
        seed_values.append(secrets.token_bytes(length))
    
    # 3. Platform-specific entropy
    platform_entropy = _get_platform_entropy(length)
    seed_values.append(platform_entropy)
    
    # 4. High security adds more sources
    if security_level in ('high', 'paranoid'):
        # Add more runtime-derived entropy
        seed_values.append(str(time.process_time()).encode())
        seed_values.append(str(threading.active_count()).encode())
    
    # 5. Paranoid mode does multiple rounds of hashing
    if security_level == 'paranoid':
        combined = b''.join(seed_values)
        result = combined
        
        # Multiple rounds of hashing
        for _ in range(3):
            result = hashlib.sha512(result).digest()
            
        # XOR with fresh entropy
        final_entropy = secrets.token_bytes(64)
        result_array = bytearray(result[:length])
        for i in range(length):
            result_array[i] ^= final_entropy[i % len(final_entropy)]
            
        return bytes(result_array)
    
    # For medium/high security, single round of hashing
    combined = b''.join(seed_values)
    return hashlib.sha512(combined).digest()[:length]


def generate_string(length, charset='hex', security_level='high', custom_chars=None):
    """
    Generate a secure random string
    
    Args:
        length: Length of the string
        charset: 'hex', 'base64', 'alphanumeric', 'printable', 'ascii', 'digits', 'url_safe', or 'custom'
        security_level: 'medium', 'high', or 'paranoid'
        custom_chars: Custom character set to use when charset='custom'
        
    Returns:
        Secure random string of specified length and character set
    """
    if length <= 0:
        raise ValueError("Length must be positive")
        
    # Handle custom character set
    if charset == 'custom':
        if not custom_chars or len(custom_chars) < 2:
            raise ValueError("Custom charset must have at least 2 characters")
        chars = custom_chars
        # Ensure enough entropy for character selection
        bytes_needed = (length * 8 + 7) // 8  # 8 bits per character for safety
        random_bytes = generate_bytes(bytes_needed, security_level)
        # Convert bytes to string using custom charset
        result = ''
        for i in range(length):
            # Use modulo to select character, extracting a byte at a time
            idx = random_bytes[i % len(random_bytes)] % len(chars)
            result += chars[idx]
        return result
    
    # Handle standard character sets
    if charset == 'hex':
        return generate_bytes((length + 1) // 2, security_level).hex()[:length]
    elif charset == 'base64':
        b64 = base64.b64encode(generate_bytes((length * 3 + 3) // 4, security_level)).decode('ascii')
        return b64[:length]
    elif charset == 'url_safe':
        # URL-safe base64 (useful for tokens in URLs)
        b64 = base64.urlsafe_b64encode(generate_bytes((length * 3 + 3) // 4, security_level)).decode('ascii')
        return b64.replace('=', '')[:length]  # Remove padding characters
    elif charset == 'alphanumeric':
        chars = string.ascii_letters + string.digits
    elif charset == 'printable':
        chars = string.ascii_letters + string.digits + string.punctuation
    elif charset == 'ascii':
        chars = string.ascii_letters
    elif charset == 'digits':
        chars = string.digits
    else:
        raise ValueError(f"Unknown charset: {charset}")
    
    # Generate with secrets module for most character sets
    # This implementation is resistant to timing attacks
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_number(bits, security_level='high'):
    """
    Generate a secure random integer
    
    Args:
        bits: Number of bits
        security_level: 'medium', 'high', or 'paranoid'
        
    Returns:
        Secure random integer with specified number of bits
    """
    if bits <= 0:
        raise ValueError("Bits must be positive")
        
    bytes_needed = (bits + 7) // 8
    value = int.from_bytes(generate_bytes(bytes_needed, security_level), byteorder='big')
    
    # Mask to ensure we don't exceed the requested bit length
    max_value = (1 << bits) - 1
    return value & max_value


def generate_password(length=16, min_digits=1, min_special=1, security_level='high'):
    """
    Generate a secure password with configurable requirements
    
    Args:
        length: Length of the password
        min_digits: Minimum number of digits required
        min_special: Minimum number of special characters required
        security_level: 'medium', 'high', or 'paranoid'
        
    Returns:
        Secure random password meeting requirements
    """
    if length < (min_digits + min_special + 1):
        raise ValueError("Password length must accommodate all minimum requirements")
    
    digits = string.digits
    special = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    letters = string.ascii_letters
    
    # Generate the base password with required character types
    password_chars = []
    
    # Add required digits
    for _ in range(min_digits):
        password_chars.append(secrets.choice(digits))
        
    # Add required special characters
    for _ in range(min_special):
        password_chars.append(secrets.choice(special))
        
    # Fill the rest with letters
    remaining = length - min_digits - min_special
    for _ in range(remaining):
        password_chars.append(secrets.choice(letters))
        
    # Shuffle the password to avoid predictable positioning
    secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)


def generate_api_key(prefix=None, length=32, security_level='high'):
    """
    Generate an API key with optional prefix
    
    Args:
        prefix: Optional prefix for the API key
        length: Length of the API key (not including prefix)
        security_level: 'medium', 'high', or 'paranoid'
        
    Returns:
        Secure API key with optional prefix
    """
    if prefix and not all(c in string.ascii_letters + string.digits + '._-' for c in prefix):
        raise ValueError("API key prefix should only contain letters, digits, dots, underscores, or hyphens")
    
    key = generate_string(length, charset='url_safe', security_level=security_level)
    
    if prefix:
        return f"{prefix}.{key}"
    return key
from CryptoStrings.core import (
    generate_string,
    generate_number,
    generate_bytes
)

print("\n🔐 SECURE STRING EXAMPLES\n" + "-"*40)
print("Base64 Token (64 chars):")
print(generate_string(64, charset='base64'))
print("\nHex Token (32 chars):")
print(generate_string(32, charset='hex'))
print("\nAlphanumeric Password (20 chars):")
print(generate_string(20, charset='alphanumeric'))
print("\nPrintable ASCII (50 chars):")
print(generate_string(50, charset='printable'))
print("\nLetters Only (A-Z, a-z, 30 chars):")
print(generate_string(30, charset='ascii'))
print("\nDigits Only (10 digits):")
print(generate_string(10, charset='digits'))

print("\n🔢 SECURE NUMBER EXAMPLES\n" + "-"*40)
print("128-bit secure number:")
print(generate_number(128))
print("\n256-bit secure number:")
print(generate_number(256))
print("\n12-bit secure number:")
print(generate_number(12))

print("\n📦 SECURE BYTES EXAMPLES\n" + "-"*40)
print("128-bit key (16 bytes, hex):")
print(generate_bytes(16).hex())
print("\n256-bit key (32 bytes, hex):")
print(generate_bytes(32).hex())
print("\n64 bytes (raw output):")
raw_bytes = generate_bytes(64)
print(f"Raw length: {len(raw_bytes)}")
print(raw_bytes)
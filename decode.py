def decode_value(bytearr):
    # Assuming little-endian format, you can try decoding these as integers
    value = int.from_bytes(bytearr, byteorder='little', signed=False)
    return value

# Example usage:
value1 = decode_value(bytearray(b'\x00\x04\x00\x01\xa0\x14\x00'))
value2 = decode_value(bytearray(b"X\x1cJ\xc3%N\'{"))
value3 = decode_value(bytearray(b'\xff\x14\x01\x00\xff5\x02\x00\x01\x01\x9c\xa1P\x00\xf2\xff\xff\xff\x00'))

print(f"Decoded value 1: {value1}")
print(f"Decoded value 2: {value2}")
print(f"Decoded value 3: {value3}")

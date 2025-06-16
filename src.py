import cv2
import numpy as np
import matplotlib.pyplot as plt

# ASCII Mapping (Ensure values remain within the range of 0-127)
d = {chr(i): i for i in range(128)}
c = {i: chr(i) for i in range(128)}

# Load Image
image_path = "A_sunflower.jpg"
x = cv2.imread(image_path)

if x is None:
    raise FileNotFoundError(f"Image at {image_path} could not be loaded.")

xrgb = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
plt.imshow(xrgb)
plt.axis("off")
plt.show()

print()

# Define Text & Key
text = "Hello"
key = "123"

text_ascii = [d[ch] for ch in text]
key_ascii = [d[ch] for ch in key]

# Encrypt using pixel modification + LSB encoding
x_enc = x.copy()
n, m, z = 0, 0, 0
l = len(text)

for i in range(l):
    kl = i % len(key)  # Ensure key loops correctly
    char_val = text_ascii[i] ^ key_ascii[kl]

    # Ensure pixel indexes stay within bounds
    if n < x_enc.shape[0] and m < x_enc.shape[1]:  
        for bit_pos in range(8):
            bit = (char_val >> (7 - bit_pos)) & 1  # Extract bit from ASCII value
            x_enc[n, m, z] = (x_enc[n, m, z] & 254) | bit  # Modify LSB
            #print(f"Embedding bit {bit} at ({n},{m},{z})")  # Debug print

            # Safe index increments
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m >= x_enc.shape[1]:
                    m = 0
                    n += 1

cv2.imwrite("encrypt.jpg", x_enc)
plt.imshow(cv2.cvtColor(x_enc, cv2.COLOR_BGR2RGB))
plt.title("Encrypted Image")
plt.axis("off")
plt.show()

# Decryption
n, m, z = 0, 0, 0
decrypt = ""

for i in range(l):
    kl = i % len(key)
    bit_value = 0

    # Ensure pixel indexes stay within bounds
    if n < x_enc.shape[0] and m < x_enc.shape[1]:  
        for bit_pos in range(8):
            bit = (x_enc[n, m, z] & 1)  # Extract stored bit
            bit_value = (bit_value << 1) | bit  # Shift bits correctly
            #print(f"Extracting bit {bit} from ({n},{m},{z})")  # Debug print

            # Safe index increments
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m >= x_enc.shape[1]:
                    m = 0
                    n += 1

    # Reverse XOR to get original ASCII character
    ascii_val = bit_value ^ key_ascii[kl]
    ascii_val = ascii_val % 128  # Ensure valid ASCII range

    decrypt += c.get(ascii_val, "?")  # Use fallback "?" for invalid characters
print()
print("Expected Text:", text)
print("Decrypted Text:", decrypt)

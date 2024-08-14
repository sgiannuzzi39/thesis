import pickle
import numpy as np

# Path to the meta.pkl file
meta_path = "/Users/sgiannuzzi/Desktop/nanoGPT-master/data/short_stories/meta.pkl"

# Load the meta.pkl file
with open(meta_path, 'rb') as f:
    meta = pickle.load(f)

itos = meta['itos']
stoi = meta['stoi']

# Function to encode a text
def encode_text(text):
    return [stoi[char] for char in text]

# Function to decode an encoded text
def decode_text(encoded_text):
    return ''.join([itos[idx] for idx in encoded_text])

# Example text to encode and decode
sample_text = "A sample text to encode and decode."

# Encode the text
encoded_sample = encode_text(sample_text)

# Decode the text
decoded_text = decode_text(encoded_sample)

print("Original Text:")
print(sample_text)
print("\nEncoded Text:")
print(encoded_sample)
print("\nDecoded Text:")
print(decoded_text)

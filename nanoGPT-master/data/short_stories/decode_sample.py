import pickle
import numpy as np

# Path to the meta.pkl file
meta_path = "/Users/sgiannuzzi/Desktop/nanoGPT-master/data/short_stories/meta.pkl"

# Load the meta.pkl file
with open(meta_path, 'rb') as f:
    meta = pickle.load(f)

itos = meta['itos']

# Function to decode an encoded text
def decode_text(encoded_text):
    return ''.join([itos[idx] for idx in encoded_text])

# Example encoded text (this should be an array of indices from your dataset)
# For demonstration purposes, I'll create a small example. Replace this with your actual encoded text.
encoded_sample = np.array([24, 49, 60, 49,  1, 61, 63,  1, 54, 63, 62, 68,  9])

# Decode the text
decoded_text = decode_text(encoded_sample)
print("Decoded Text:")
print(decoded_text)

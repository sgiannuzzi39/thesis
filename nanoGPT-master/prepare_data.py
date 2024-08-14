import os
import pickle
import numpy as np

# Define the paths
input_file_path = "/Users/sgiannuzzi/Desktop/nanoGPT-master/input/txts/input.txt"
output_dir = "/Users/sgiannuzzi/Desktop/nanoGPT-master/data/short_stories"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the input text file
with open(input_file_path, "r", encoding="utf-8") as f:
    data = f.read()

# Create character-level vocabulary
chars = sorted(list(set(data)))
vocab_size = len(chars)
print(f"Vocab size: {vocab_size}")

# Create mappings from character to index and vice versa
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

# Encode the dataset
encoded_data = np.array([stoi[c] for c in data], dtype=np.uint16)

# Split into train and validation sets
n = len(encoded_data)
train_data = encoded_data[:int(n*0.9)]
val_data = encoded_data[int(n*0.9):]

# Save the data to binary files
train_bin_path = os.path.join(output_dir, "train.bin")
val_bin_path = os.path.join(output_dir, "val.bin")

train_data.tofile(train_bin_path)
val_data.tofile(val_bin_path)

# Save the meta information
meta = {
    "vocab_size": vocab_size,
    "itos": itos,
    "stoi": stoi,
}
meta_path = os.path.join(output_dir, "meta.pkl")
with open(meta_path, "wb") as f:
    pickle.dump(meta, f)

print("Data preparation is complete.")

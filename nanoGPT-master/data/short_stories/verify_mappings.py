import pickle

# Path to the meta.pkl file
meta_path = "/Users/sgiannuzzi/Desktop/nanoGPT-master/data/short_stories/meta.pkl"

# Load the meta.pkl file
with open(meta_path, 'rb') as f:
    meta = pickle.load(f)

itos = meta['itos']
stoi = meta['stoi']

# Print the mappings to verify
print("Index to String Mapping (itos):")
for index, char in itos.items():
    print(f"{index}: '{char}'")

print("\nString to Index Mapping (stoi):")
for char, index in stoi.items():
    print(f"'{char}': {index}")

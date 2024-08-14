import pickle

# Path to the meta.pkl file
meta_path = "/Users/sgiannuzzi/Desktop/nanoGPT-master/data/short_stories/meta.pkl"

# Load the meta.pkl file
with open(meta_path, 'rb') as f:
    meta = pickle.load(f)

# Print the content of the meta file in a more readable format
print("Meta Information:")
print(f"Vocab Size: {meta['vocab_size']}")

print("\nIndex to String Mapping (itos):")
for index, char in meta['itos'].items():
    print(f"{index}: '{char}'")

print("\nString to Index Mapping (stoi):")
for char, index in meta['stoi'].items():
    print(f"'{char}': {index}")

import torch
from transformers import GPT2LMHeadModel, GPT2Config

# Path to your fine-tuned model
model_path = "/Users/sgiannuzzi/Desktop/thesis/generator-from-scratch/fine_tuned_gpt2"

# Load the model
print("Loading the model...")
model = GPT2LMHeadModel.from_pretrained(model_path)

# Update the configuration
print("Updating configuration...")
model.config.n_positions = 1024  # Set to the correct value
model.transformer.wpe = torch.nn.Embedding(1024, model.config.n_embd)

# Save the updated model
print("Saving the updated model...")
model.save_pretrained(model_path)
print("Positional embeddings updated and model saved successfully!")

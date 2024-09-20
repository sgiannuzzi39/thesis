"""

makes two datasets: 

first is embeddings of all words in a txt file, saved to total_embeddings folder

second is embeddings of two sets of words: all words in sentences before last 10 sentences, and all words in last 10 sentences, saved to endings_embeddings

"""

import os
import torch
from transformers import GPT2Tokenizer, GPT2Model

# Load pre-trained GPT model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

# Ensure output folders exist
if not os.path.exists("embeddings/generated/total_embeddings"):
    os.makedirs("embeddings/generated/total_embeddings")

if not os.path.exists("embeddings/generated/endings_embeddings"):
    os.makedirs("embeddings/generated/endings_embeddings")

def load_text_from_file(file_path):
    """
    Loads the text from a .txt file.
    
    Args:
        file_path (str): Path to the .txt file.
        
    Returns:
        str: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_total_embeddings(file_name, embeddings):
    """
    Save embeddings for the entire text file into a .txt file.

    Args:
        file_name (str): Name of the file to save the embeddings.
        embeddings (list): List of word embeddings.
    """
    # Correct the path to match the created directory
    file_path = os.path.join("embeddings/generated/total_embeddings", f"{file_name}_embeddings.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        for word_embedding in embeddings:
            f.write(f"{word_embedding.tolist()}\n")

def save_split_embeddings(file_name, first_part, last_part):
    """
    Save the embeddings split into two arrays: one for the sentences before the last 10 sentences,
    and one for the last 10 sentences.

    Args:
        file_name (str): Name of the file to save the embeddings.
        first_part (list): List of embeddings for sentences before the last 10 sentences.
        last_part (list): List of embeddings for the last 10 sentences.
    """
    # Correct the path to match the created directory
    file_path = os.path.join("embeddings/generated/endings_embeddings", f"{file_name}_split_embeddings.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("First Part Embeddings:\n")
        for embedding in first_part:
            f.write(f"{embedding.tolist()}\n")
        
        f.write("\nLast 10 Sentences Embeddings:\n")
        for embedding in last_part:
            f.write(f"{embedding.tolist()}\n")


def embed_text(text):
    """
    Get embeddings for each word in the text.

    Args:
        text (str): The input text.
    
    Returns:
        list: A list of embeddings for each token in the text.
    """
    # Assign eos_token as the pad_token for GPT-2
    tokenizer.pad_token = tokenizer.eos_token

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    
    # Get model outputs
    outputs = model(**inputs)
    
    # Extract the embeddings for all tokens
    embeddings = outputs.last_hidden_state[0]  
    
    return embeddings


def split_text(text):
    """
    Split the text into all sentences before the last 10 sentences and the last 10 sentences.

    Args:
        text (str): The input text.

    Returns:
        tuple: Two parts of the text: first part before the last 10 sentences, and last 10 sentences.
    """
    sentences = text.split(".")  # Simple sentence split based on period.
    sentences = [s.strip() for s in sentences if s.strip()]  # Clean empty or whitespace sentences
    
    # If there are 10 or fewer sentences, all of them should be in the last part, and the first part should be empty
    if len(sentences) <= 10:
        first_part = []
        last_part = sentences
    else:
        first_part = sentences[:-10]
        last_part = sentences[-10:]
    
    return first_part, last_part


def embed_and_save(file_path):
    """
    Embed the text, save the total embeddings, and split the embeddings for the first part and last 10 sentences.
    
    Args:
        file_path (str): Path to the .txt file.
    """
    text = load_text_from_file(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Embed the entire text
    total_embeddings = embed_text(text)
    
    # Save total embeddings in one file
    save_total_embeddings(file_name, total_embeddings)
    
    # Split text into two parts: first part and last 10 sentences
    first_part_text, last_part_text = split_text(text)
    
    # Embed first part and last part separately
    first_part_embeddings = embed_text(". ".join(first_part_text))  # Joining back sentences
    last_part_embeddings = embed_text(". ".join(last_part_text))
    
    # Save split embeddings into two arrays in a single file
    save_split_embeddings(file_name, first_part_embeddings, last_part_embeddings)

# Example usage:
if __name__ == "__main__":
    folder_path = "generated-stories/"  # Replace with the path to your folder of .txt files
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            embed_and_save(file_path)

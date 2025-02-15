# conda activate new_env

import os
import re
from datetime import datetime
from src.load_data import load_txt_files  # Assuming these are already implemented
from src.preprocess import preprocess_stories
from src.generate_story import generate_story
from src.train_model import fine_tune_model

def count_words(text):
    """Helper function to count words in a text."""
    return len(re.findall(r'\b\w+\b', text))

def main():
    print("Starting AI Story Generator...")

    # Load the data
    txt_directory = 'data/txt_files'
    print(f"Loading text files from {txt_directory}...")
    stories = load_txt_files(txt_directory)
    print(f"Loaded {len(stories)} stories.")

    if not stories:
        print("No stories loaded. Please check the txt_files directory.")
        return

    # Preprocess the data
    print("Preprocessing stories...")
    preprocessed_stories = preprocess_stories(stories)
    print("Preprocessing complete.")

    # Create a corpus (not used in this version but kept for potential future use)
    print("Creating corpus...")
    corpus = ""
    for story in preprocessed_stories:
        corpus += f"{story['content']}\n\n"
    print("Corpus created.")

    # Generate 15 stories based on a simple prompt using GPT-4
    print("Generating 15 stories...")
    min_word_count = 1000
    max_word_count = 7500

    for i in range(1):
        print(f"Generating story {i+1}...")

        title, generated_story = generate_story(prompt="Write a short story.", min_length=min_word_count, max_length=max_word_count)

        # Check the word count of the generated story
        word_count = count_words(generated_story)
        if word_count < min_word_count:
            print(f"Warning: Generated story {i+1} has only {word_count} words, which is below the minimum of {min_word_count} words.")
        elif word_count > max_word_count:
            print(f"Warning: Generated story {i+1} has {word_count} words, which exceeds the maximum of {max_word_count} words.")

        # Check if the generated story starts with "Once upon a time"
        if generated_story.lower().startswith("once upon a time"):
            # Modify the start if needed
            print(f"Story {i+1} starts with 'Once upon a time'. Modifying the start...")
            generated_story = generated_story[len("once upon a time"):].strip().capitalize()

        # Save each generated story to a file regardless of word count
        save_generated_story(title, generated_story, len(stories), i+1)

def save_generated_story(title, generated_story, story_count, story_number):
    """Saves the generated story to a file."""
    # Ensure the directory exists
    os.makedirs('stories_generated', exist_ok=True)

    # Create the filename with a timestamp and the story number
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stories_generated/generated_story_{story_number}_{timestamp}.txt"

    # Prepare the content to save
    content = f"Fine Tuned GPT-4\n{datetime.now().strftime('%B %dth, %Y')}\n{story_count} stories\n\n"
    content += f"{generated_story}"

    # Save to file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Story {story_number} saved to {filename}")

if __name__ == "__main__":
    main()

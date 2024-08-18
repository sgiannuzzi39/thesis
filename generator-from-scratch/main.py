import os
import re
from datetime import datetime
from src.load_data import load_txt_files
from src.preprocess import preprocess_stories
from src.generate_story import generate_story
from src.train_model import fine_tune_model

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

    # Generate a story based on a simple prompt using GPT-4
    print("Generating a story...")
    title, generated_story = generate_story(prompt="Write a short story.", min_length=1000, max_length=7500)
    print("Generated Story:\n")
    print(generated_story)

    # Save the generated story to a file
    save_generated_story(title, generated_story, len(stories))

def save_generated_story(title, generated_story, story_count):
    # Ensure the directory exists
    os.makedirs('stories_generated', exist_ok=True)

    # Create the filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stories_generated/generated_story_{timestamp}.txt"

    # Prepare the content to save
    content = f"Fine Tuned GPT-4\n{datetime.now().strftime('%B %dth, %Y')}\n{story_count} stories\n\n"
    content += f"{generated_story}"

    # Save to file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Story saved to {filename}")

if __name__ == "__main__":
    main()

from src.load_data import load_txt_files
from src.preprocess import preprocess_stories
from src.train_model import fine_tune_model
from src.generate_story import generate_story
import os
os.environ["WANDB_DISABLED"] = "true"


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

    # Create a corpus
    print("Creating corpus...")
    corpus = ""
    for story in preprocessed_stories:
        corpus += f"Title: {story['title']}\nAuthor: {story['author']}\n\n{story['content']}\n\n"
    print("Corpus created.")

    # Fine-tune the model
    print("Fine-tuning the model...")
    fine_tune_model(corpus)
    print("Model fine-tuning complete.")

    # Generate a story based on a prompt
    print("Generating a story...")
    prompt = """Title: The Dark Night
Author: Emily Bronte

The wind howled through the ancient trees, carrying with it the whispers of forgotten tales. In the heart of the forest, a young woman wandered, lost not only in the woods but in the labyrinth of her thoughts..."""
    generated_story = generate_story(prompt)
    print("Generated Story:\n")
    print(generated_story)

if __name__ == "__main__":
    main()

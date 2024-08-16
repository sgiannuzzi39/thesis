from src.load_data import load_txt_files
from src.preprocess import preprocess_stories
from src.train_model import fine_tune_model
from src.generate_story import generate_story
import os
from datetime import datetime

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
    prompt = """Title: The Button
Author: John Doe

Mr. Smithson was not accustomed to the esteemed ways of higher society. In fact, ..."""
    generated_story = generate_story(prompt)
    print("Generated Story:\n")
    print(generated_story)

    # Save the generated story to a file
    save_generated_story(prompt, generated_story, len(stories))

def save_generated_story(prompt, generated_story, story_count):
    # Ensure the directory exists
    os.makedirs('stories_generated', exist_ok=True)

    # Create the filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stories_generated/generated_story_{timestamp}.txt"

    # Prepare the content to save
    content = f"Fine Tuned GPT-2\n{datetime.now().strftime('%B %dth, %Y')}\n{story_count} stories\n\n"
    content += f"Prompt: \"{prompt.strip()}\"\n\nGenerated Story:\n\n"
    content += generated_story

    # Save to file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Story saved to {filename}")

if __name__ == "__main__":
    main()

import os
import re
from datetime import datetime
from src.generate_story import generate_story

def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

def main(fine_tune=False):
    print("Starting AI Story Generator...")

    model_output_dir = "/Users/sgiannuzzi/Desktop/thesis/generator-from-scratch/fine_tuned_gpt2"

    if fine_tune:
        from src.train_model import fine_tune_model

        txt_directory = "/Users/sgiannuzzi/Desktop/thesis/generator-from-scratch/data/txt_files"
        print("Fine-tuning GPT-2 model...")
        fine_tune_model(corpus_path=txt_directory, output_dir=model_output_dir)
        print("Fine-tuning complete. Model saved.")

    print("Generating a story...")
    min_word_count = 1000
    max_word_count = 7500

    title, generated_story = generate_story(
        prompt="Write a short story.",
        min_length=min_word_count,
        max_length=max_word_count,
        model_dir=model_output_dir
    )

    word_count = count_words(generated_story)
    if word_count < min_word_count:
        print(f"Warning: Generated story has only {word_count} words, which is below the minimum of {min_word_count} words.")
    elif word_count > max_word_count:
        print(f"Warning: Generated story has {word_count} words, which exceeds the maximum of {max_word_count} words.")

    if generated_story.lower().startswith("once upon a time"):
        print("Story starts with 'Once upon a time'. Modifying the start...")
        generated_story = generated_story[len("once upon a time"):].strip().capitalize()

    print("Generated Story:\n")
    print(generated_story)

    save_generated_story(title, generated_story)

def save_generated_story(title, generated_story):
    os.makedirs('stories_generated', exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stories_generated/generated_story_{timestamp}.txt"

    content = f"Fine Tuned GPT-2\n{datetime.now().strftime('%B %dth, %Y')}\n\n"
    content += f"{generated_story}"

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(content)

    print(f"Story saved to {filename}")

if __name__ == "__main__":
    main(fine_tune=False)

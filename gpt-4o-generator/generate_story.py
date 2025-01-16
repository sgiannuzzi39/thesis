import openai
import os
from datetime import datetime

openai.api_key = "___"

def generate_short_story():
    """
    Generate a short story using OpenAI's GPT-4 model.

    Returns:
    - tuple: The title and the content of the generated short story.
    """
    try:
        # Define the prompt for GPT-4
        prompt = "You are a short story writer. Write a short story between 1000-7500 words long."

        # API call to generate the story
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the title and story content
        story = response.choices[0].message.content.strip()
        title_line = story.split("\n", 1)[0]  # First line as title
        title = title_line.replace("Title: ", "").strip()
        return title, story
    except Exception as e:
        print(f"Error generating story: {e}")
        return None, None

def format_title_as_filename(title):
    """
    Convert the story title into snake_case for the filename.

    Parameters:
    - title (str): The title of the story.

    Returns:
    - str: The formatted filename.
    """
    sanitized_title = "".join(c if c.isalnum() or c in " -" else "" for c in title)  # Remove special characters
    snake_case_title = sanitized_title.replace(" ", "_").replace("-", "_").lower()  # Convert to snake_case
    return snake_case_title or "untitled_story"

def save_story_to_file(title, story, folder="/Users/sgiannuzzi/Desktop/thesis/gpt-4o-generator/generated_stories"):
    """
    Save the generated story to a text file in the specified folder.

    Parameters:
    - title (str): The title of the story (used for the filename).
    - story (str): The story content.
    - folder (str): The folder to save the story in.
    """
    os.makedirs(folder, exist_ok=True)

    # Format title as snake_case for the filename
    filename = f"{format_title_as_filename(title)}.txt"
    filepath = os.path.join(folder, filename)

    # Save the story to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(story)

    print(f"Story saved as {filepath}")

def main():
    print("Generating story...")

    # Generate the story
    title, story = generate_short_story()

    if title and story:
        print("\nGenerated Story (Preview):\n")
        print(story[:500] + "\n...")  # Display a preview of the story
        save_story_to_file(title, story)
    else:
        print("Failed to generate the story.")

if __name__ == "__main__":
    main()

"""
    Code co-authored with ChatGPT
    conda activate new_env
"""

from openai import OpenAI
import os

client = OpenAI(api_key="___")

def generate_story_part(prompt, max_tokens=4000):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating story part: {e}")
        return None

def save_story_to_file(filename, content, folder="/Users/sgiannuzzi/Desktop/thesis/gpt-4-generated_stories"):

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    base, ext = os.path.splitext(filepath)
    counter = 1
    while os.path.exists(filepath):
        filepath = f"{base}{counter}{ext}"
        counter += 1

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Story saved as {filepath}")

def extract_and_format_title(story_text, max_length=50):

    first_line = story_text.splitlines()[0].strip()
    if first_line.lower().startswith("title"):
        first_line = first_line[5:].strip()
    formatted_title = "".join(c if c.isalnum() or c in " _-" else "" for c in first_line).replace(" ", "_")
    return formatted_title[:max_length]

def generate_and_save_story(index):

    first_half_prompt = (
        "You are a professional short story writer. Write the first half of a story that is at least 1,000 words long."
    )
    first_half = generate_story_part(first_half_prompt)

    if first_half:
        second_half_prompt = (
            f"{first_half}\n\n"
            "Continue this story without explicitly stating that it is a continuation. "
            "Keep the tone and style consistent with the first half."
            "The length of the story is unimportant - it should be as long as feels right for the plot."
        )
        second_half = generate_story_part(second_half_prompt)

        if second_half:
            story_content = f"{first_half}\n\n{second_half}"
            story_title = extract_and_format_title(first_half)
            filename = f"{story_title}_{index}.txt"  
            save_story_to_file(filename, story_content)
        else:
            print(f"Failed to generate the second half of story {index}.")
    else:
        print(f"Failed to generate the first half of story {index}.")

def main():
    for i in range(1, 12):  
        print(f"Generating story {i}...")
        generate_and_save_story(i)

if __name__ == "__main__":
    main()
import os
import requests
from bs4 import BeautifulSoup

# Base URL of the website
base_url = "https://americanliterature.com"

# URL of the page containing links to the short stories
story_list_url = base_url + "/100-great-short-stories/"

# Create a directory to save the short stories
if not os.path.exists("short_stories"):
    os.makedirs("short_stories")

# Function to save story content to a text file
def save_story(title, author, content):
    # Extract the author's last name (assuming the last word is the last name)
    last_name = author.split()[-1]
    filename = f"short_stories/{title}, {last_name}.txt".replace(" ", "_").replace(":", "")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Author: {author}\n\n")
        f.write(content)

# Function to extract and save a short story
def extract_story(story_url):
    response = requests.get(story_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title and author
    title = soup.find("h1", itemprop="name").text.strip()
    author = soup.find("a", itemprop="author").text.strip()

    # Extract the story content
    story_paragraphs = soup.find_all("p")
    story_content = "\n\n".join([para.text for para in story_paragraphs])

    # Remove any unwanted content (like library links, next story prompts, etc.)
    unwanted_phrases = ["to your library.", "Return to the", "Or read more short stories"]
    for phrase in unwanted_phrases:
        story_content = story_content.split(phrase)[0]

    # Save the story to a text file
    save_story(title, author, story_content)

# Function to find all story links and extract them
def scrape_stories():
    response = requests.get(story_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all story links
    story_links = soup.find_all("a", href=True)

    for link in story_links:
        if "/short-story/" in link['href']:
            story_url = base_url + link['href']
            extract_story(story_url)

# Start the scraping process
scrape_stories()

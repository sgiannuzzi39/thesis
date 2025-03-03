''' 
    Code co-authored with ChatGPT
'''

import os
import requests
from bs4 import BeautifulSoup

# base URL of the website
base_url = "https://americanliterature.com"

# URL of the page containing links to the short stories
story_list_url = base_url + "/100-great-short-stories/"

# directory to save the short stories
if not os.path.exists("short_stories"):
    os.makedirs("short_stories")

# save story content to a text file
def save_story(title, author, content):
    # author's last name 
    last_name = author.split()[-1]
    filename = f"short_stories/{title}, {last_name}.txt".replace(" ", "_").replace(":", "")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Author: {author}\n\n")
        f.write(content)

# extract and save a short story
def extract_story(story_url):
    response = requests.get(story_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # title and author
    title = soup.find("h1", itemprop="name").text.strip()
    author = soup.find("a", itemprop="author").text.strip()

    # story content
    story_paragraphs = soup.find_all("p")
    story_content = "\n\n".join([para.text for para in story_paragraphs])

    # remove unwanted content 
    unwanted_phrases = ["to your library.", "Return to the", "Or read more short stories"]
    for phrase in unwanted_phrases:
        story_content = story_content.split(phrase)[0]

    # save the story 
    save_story(title, author, story_content)

# find all story links and extract them
def scrape_stories():
    response = requests.get(story_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # all story links
    story_links = soup.find_all("a", href=True)

    for link in story_links:
        if "/short-story/" in link['href']:
            story_url = base_url + link['href']
            extract_story(story_url)

scrape_stories()

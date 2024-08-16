import os
import re
import requests
from bs4 import BeautifulSoup

# Set the output directory for saving the text files
output_directory = "output_stories"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Base URL for the website
base_url = "https://classicshorts.com"

# List of letter groups to process
letter_groups = ['a-d', 'e-h', 'i-m', 'n-s', 't-z']

def clean_author_name(author):
    # Remove any years in parentheses from the author's name
    return re.sub(r'\s*\(.*?\)', '', author).strip()

def extract_lastname(author):
    # Extract the last name of the author
    clean_author = clean_author_name(author)
    return clean_author.split()[-1]

def save_story(title, author, story_content):
    # Clean the author's name (remove years) for the content
    clean_author = clean_author_name(author)
    
    # Get the author's last name
    lastname = extract_lastname(author)
    
    # Format the title and author last name to ensure no underscores and only spaces
    formatted_title = title.replace("_", " ").replace(":", " -")
    
    # Format the filename according to the naming convention
    filename = f"{output_directory}/{formatted_title}, {lastname}.txt"
    
    # Save the story to a text file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Author: {clean_author}\n\n")  # Write the cleaned author name without years
        f.write(story_content)

def extract_story(story_url):
    response = requests.get(story_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title
    title_element = soup.find("div", onclick="gotoSpecificBib()")
    title = title_element.get_text(strip=True)

    # Extract the author
    author_element = soup.find("span", style="font-weight:500;")
    author = author_element.get_text(strip=True)

    # Extract the story content
    paragraphs = soup.find_all("div", class_="StoryPara")
    story_content = "\n".join([para.get_text(strip=True) for para in paragraphs])

    # Save the story
    save_story(title, author, story_content)

def crawl_stories():
    # Iterate over each letter group
    for group in letter_groups:
        # Open the page for the current letter group
        response = requests.get(f"{base_url}/abc/{group}.html")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Collect all story links
        stories = soup.find_all("div", onclick=lambda value: value and value.startswith("openStory"))
        
        for story in stories:
            story_relative_url = story['onclick'].split("'")[1]
            story_url = f"{base_url}{story_relative_url}"
            extract_story(story_url)

# Start the web crawling process
crawl_stories()

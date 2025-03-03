''' 
    Code co-authored with ChatGPT
'''

import os
import re
import requests
from bs4 import BeautifulSoup

# output directory 
output_directory = "output_stories"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# base URL 
base_url = "https://classicshorts.com"

# letter groups to process
letter_groups = ['a-d', 'e-h', 'i-m', 'n-s', 't-z']

def clean_author_name(author):
    # clean the name
    return re.sub(r'\s*\(.*?\)', '', author).strip()

def extract_lastname(author):
    # extra last name 
    clean_author = clean_author_name(author)
    return clean_author.split()[-1]

def save_story(title, author, story_content):
    
    clean_author = clean_author_name(author)
    lastname = extract_lastname(author)
    
    # format the title and author last name 
    formatted_title = title.replace("_", " ").replace(":", " -")
    
    # format the filename
    filename = f"{output_directory}/{formatted_title}, {lastname}.txt"
    
    # save the story 
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Author: {clean_author}\n\n") 
        f.write(story_content)

def extract_story(story_url):
    response = requests.get(story_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract title
    title_element = soup.find("div", onclick="gotoSpecificBib()")
    title = title_element.get_text(strip=True)

    # extract author
    author_element = soup.find("span", style="font-weight:500;")
    author = author_element.get_text(strip=True)

    # extract story content
    paragraphs = soup.find_all("div", class_="StoryPara")
    story_content = "\n".join([para.get_text(strip=True) for para in paragraphs])

    # save story
    save_story(title, author, story_content)

def crawl_stories():

    for group in letter_groups:
        # open page for current letter group
        response = requests.get(f"{base_url}/abc/{group}.html")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # collect story links
        stories = soup.find_all("div", onclick=lambda value: value and value.startswith("openStory"))
        
        for story in stories:
            story_relative_url = story['onclick'].split("'")[1]
            story_url = f"{base_url}{story_relative_url}"
            extract_story(story_url)

crawl_stories()

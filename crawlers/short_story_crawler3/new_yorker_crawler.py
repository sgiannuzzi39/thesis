import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create directory to save stories
output_dir = 'new_yorker_stories/new_yorker_page19_28'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize WebDriver
driver = webdriver.Chrome()

# Step 1: Navigate to the New Yorker fiction page
start_url = 'https://www.newyorker.com/magazine/fiction?page=27'
driver.get(start_url)
print(f"Accessed page")

# Step 2: Click on the Sign In link using XPath
sign_in_link = driver.find_element(By.XPATH, '//a[contains(text(), "Sign In")]')
sign_in_link.click()
time.sleep(2)  # Wait for the sign-in page to load
print(f"Clicked sign in")

# Step 3: Enter the email address
email_input = driver.find_element(By.ID, 'TextField-id-email')
email_input.send_keys('sgiannuzzi39@gmail.com')
email_input.send_keys(Keys.RETURN)
time.sleep(2)  # Wait for the password page to load
print(f"Entered email")

# Step 4: Enter the password
password_input = driver.find_element(By.ID, 'TextField-id-password')
password_input.send_keys('SmithSoap_86')
password_input.send_keys(Keys.RETURN)
time.sleep(2)  # Wait for the sign-in process to complete
print(f"Entered password")

# Function to scrape and save a single story
def scrape_story(story_url):
    print(f"Scraping story: {story_url}")
    response = requests.get(story_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title_tag = soup.find('h1', {'data-testid': 'ContentHeaderHed'})
    title = title_tag.text.strip() if title_tag else 'Unknown Title'
    
    # Extract author
    author_tag = soup.find('a', {'class': 'BylineLink-gEnFiw'})
    author = author_tag.text.strip() if author_tag else 'Unknown Author'
    
    # Extract story content, ensuring the first paragraph is captured
    story_paragraphs = soup.find_all('p', class_=lambda x: x and 'paywall' in x.split())
    story_content = "\n\n".join([
        p.text.strip() for p in story_paragraphs 
        if p.find('a') is None and p.find('strong') is None
    ])
    
    # Prepare the file name
    author_lastname = author.split()[-1]
    file_name = os.path.join(output_dir, f"{title}, {author_lastname}.txt")
    
    # Save to a text file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"Title: {title}\n")
        file.write(f"Author: {author}\n\n")
        file.write(story_content)
    
    print(f"Saved story to {file_name}")

# Function to crawl the main fiction page
def crawl_fiction_page(start_url):
    print(f"Accessing {start_url}...")
    driver.get(start_url)
    
    stories_scraped = 0
    page_number = 27  # Start from page 18
    
    while True:  # Continue until no more pages are found
        print("Scraping page...")
        
        # Wait for the story links to load
        try:
            story_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.SummaryItemHedLink-civMjp'))
            )
        except Exception as e:
            print(f"Error finding story links: {e}")
            break
        
        # Loop through the links and scrape each story
        for link in story_links:
            story_url = link.get_attribute('href')
            scrape_story(story_url)
            stories_scraped += 1
            time.sleep(1)  # To avoid overwhelming the server
        
        # Try to go to the next page
        page_number += 1
        next_page_url = f'https://www.newyorker.com/magazine/fiction?page={page_number}'
        print(f"Navigating to page {page_number}")
        
        try:
            driver.get(next_page_url)
            time.sleep(3)  # Wait for the next page to load
        except Exception as e:
            print(f"No more pages to navigate or error navigating: {e}")
            break  # No more pages to navigate
    
    print(f"Scraped {stories_scraped} stories.")

# Start crawling
try:
    crawl_fiction_page(start_url)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

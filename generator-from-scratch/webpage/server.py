import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from src.generate_story import generate_story
from src.load_data import load_txt_files
from src.train_model import fine_tune_model

def get_authors(directory):
    authors = set()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            author = filename.split(', ')[-1].replace('.txt', '')
            authors.add(author)
    return sorted(authors)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/get-authors':
            authors = get_authors('/path/to/your/txt_files')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"authors": authors}).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/generate-story':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            selected_authors = data.get('authors', [])
            selected_genres = data.get('genres', [])
            character_count = data.get('characters', 1)
            story_directory = '/path/to/your/txt_files'
            selected_stories = []

            for author in selected_authors:
                for filename in os.listdir(story_directory):
                    if filename.endswith(".txt") and author in filename:
                        with open(os.path.join(story_directory, filename), 'r', encoding='utf-8') as file:
                            selected_stories.append(file.read())

            if not selected_stories:
                selected_stories = ["No stories available for the selected authors."]

            if selected_stories:
                corpus = "\n\n".join(selected_stories)
                fine_tune_model(corpus)
                genre_prompt = ", ".join(selected_genres)
                prompt = f"Generate a {genre_prompt} short story with {character_count} main characters."
                title, generated_story = generate_story(prompt=prompt)
            else:
                title, generated_story = "No Story Generated", "Please select at least one author."

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"story": generated_story}).encode('utf-8'))

PORT = 8000
with HTTPServer(('localhost', PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

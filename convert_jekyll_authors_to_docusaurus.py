import os
import yaml
import json
from pathlib import Path

# Configuration
JEKYLL_AUTHORS_PATH = os.path.join(os.path.dirname(__file__), 'blog-jekyll', '_data', 'authors.yml')
DOCUSAURUS_AUTHORS_DIR = os.path.join(os.path.dirname(__file__), 'aks-blog', 'blog', 'authors')

def convert_jekyll_authors_to_docusaurus():
    print(f"Converting authors from {JEKYLL_AUTHORS_PATH} to Docusaurus format...")
    
    # Make sure the target directory exists
    os.makedirs(DOCUSAURUS_AUTHORS_DIR, exist_ok=True)
    
    # Read Jekyll authors data
    try:
        with open(JEKYLL_AUTHORS_PATH, 'r', encoding='utf-8') as file:
            jekyll_authors = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading Jekyll authors file: {e}")
        return
    
    if not jekyll_authors:
        print("No authors found in the Jekyll file.")
        return
    
    print(f"Found {len(jekyll_authors)} authors to convert.")
    
    # Process each author
    for author_key, author_data in jekyll_authors.items():
        try:
            convert_author(author_key, author_data)
        except Exception as e:
            print(f"Error processing author {author_key}: {e}")

def convert_author(author_key, author_data):
    # Create a safe file name
    author_id = author_key.lower().replace(" ", "-")
    
    # Create Docusaurus author data structure
    docusaurus_author = {
        "name": author_data.get("name", author_key),
        "title": author_data.get("bio", ""),
        "url": get_author_url(author_data),
        "image_url": author_data.get("avatar", "")
    }
    
    # Remove empty values
    docusaurus_author = {k: v for k, v in docusaurus_author.items() if v}
    
    # Create author JSON file
    output_file = os.path.join(DOCUSAURUS_AUTHORS_DIR, f"{author_id}.json")
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(docusaurus_author, file, indent=2)
    
    print(f"Created author file: {output_file}")

def get_author_url(author_data):
    """Extract the most relevant URL for the author"""
    if not author_data.get("links"):
        return ""
    
    # Priority order: GitHub, LinkedIn, Website, X/Twitter, Email
    url_priority = {
        "GitHub": 1,
        "LinkedIn": 2,
        "Blog": 3,
        "X": 4,
        "Email": 5
    }
    
    links = author_data.get("links", [])
    if not links:
        return ""
    
    # Sort links by priority
    sorted_links = sorted(links, key=lambda x: url_priority.get(x.get("label", ""), 999))
    
    # Return the highest priority URL
    if sorted_links:
        return sorted_links[0].get("url", "")
    
    return ""

# Create an index.js file for Docusaurus
def create_authors_index():
    index_path = os.path.join(DOCUSAURUS_AUTHORS_DIR, 'index.js')
    
    # List all JSON files in the authors directory
    author_files = [f for f in os.listdir(DOCUSAURUS_AUTHORS_DIR) if f.endswith('.json')]
    
    # Create the index.js content
    content = "// Auto-generated index file for authors\n\n"
    
    for author_file in author_files:
        author_id = author_file.replace('.json', '')
        content += f"import {author_id} from './{author_file}';\n"
    
    content += "\nexport default {\n"
    for author_file in author_files:
        author_id = author_file.replace('.json', '')
        content += f"  '{author_id}': {author_id},\n"
    content += "};\n"
    
    # Write the index.js file
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Created authors index.js file: {index_path}")

if __name__ == "__main__":
    convert_jekyll_authors_to_docusaurus()
    create_authors_index()
    print("Author conversion completed.")
import os
import re
import shutil
import yaml
import datetime
from pathlib import Path

# Configuration
JEKYLL_DIR = os.path.join(os.path.dirname(__file__), 'blog-jekyll')
DOCUSAURUS_DIR = os.path.join(os.path.dirname(__file__), 'aks-blog', 'blog')
DOCUSAURUS_ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'aks-blog', 'static', 'img', 'blog')

# Ensure the target directories exist
os.makedirs(DOCUSAURUS_DIR, exist_ok=True)
os.makedirs(DOCUSAURUS_ASSETS_DIR, exist_ok=True)

# Helper function to convert Jekyll date to Docusaurus format
def convert_date(jekyll_date):
    if isinstance(jekyll_date, datetime.datetime):
        return jekyll_date.strftime('%Y-%m-%d')
    elif isinstance(jekyll_date, str):
        # Try to parse the date string
        try:
            date_obj = datetime.datetime.strptime(jekyll_date, '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            try:
                date_obj = datetime.datetime.strptime(jekyll_date, '%Y-%m-%d %H:%M:%S')
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                # Return as is if parsing fails
                return jekyll_date
    return jekyll_date

# Process the files
def process_jekyll_files():
    print(f"Looking for Markdown files in {JEKYLL_DIR}...")
    jekyll_files = []
    
    # Find all markdown files in Jekyll directory and subdirectories
    for root, _, files in os.walk(JEKYLL_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                jekyll_files.append(os.path.join(root, file))
    
    print(f"Found {len(jekyll_files)} markdown files to process.")
    
    for file_path in jekyll_files:
        try:
            convert_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# Convert a single file
def convert_file(file_path):
    print(f"Converting {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\s+(.*?)\s+---\s+(.*)', content, re.DOTALL)
    if not frontmatter_match:
        print(f"No frontmatter found in {file_path}, skipping...")
        return
    
    frontmatter_content = frontmatter_match.group(1)
    post_content = frontmatter_match.group(2)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_content)
    except yaml.YAMLError as e:
        print(f"Error parsing frontmatter in {file_path}: {e}")
        return
    
    # Create Docusaurus frontmatter
    docusaurus_frontmatter = {}
    
    # Convert commonly used fields
    if 'title' in frontmatter:
        docusaurus_frontmatter['title'] = frontmatter['title']
    
    # Convert date
    if 'date' in frontmatter:
        docusaurus_frontmatter['date'] = convert_date(frontmatter['date'])
    
    # Convert authors
    if 'authors' in frontmatter:
        docusaurus_frontmatter['authors'] = frontmatter['authors']
    elif 'author' in frontmatter:
        docusaurus_frontmatter['authors'] = [frontmatter['author']]
    
    # Convert tags
    if 'tags' in frontmatter:
        docusaurus_frontmatter['tags'] = frontmatter['tags']
    elif 'categories' in frontmatter:
        docusaurus_frontmatter['tags'] = frontmatter['categories']
    
    # Convert slug/permalink
    if 'permalink' in frontmatter:
        slug = frontmatter['permalink'].strip('/')
        slug = slug.split('/')[-1]  # Get the last part of the permalink
        docusaurus_frontmatter['slug'] = slug
    
    # Optional: description
    if 'description' in frontmatter:
        docusaurus_frontmatter['description'] = frontmatter['description']
    elif 'excerpt' in frontmatter:
        docusaurus_frontmatter['description'] = frontmatter['excerpt']
    
    # Process image links in content
    # This is a simple replacement strategy - may need adjustment based on your specific Jekyll setup
    def process_image_links(content):
        # Pattern for Markdown image syntax: ![alt text](/path/to/image.jpg)
        img_pattern = r'!\[(.*?)\]\(([^)]+)\)'
        
        def replace_img_path(match):
            alt_text = match.group(1)
            img_path = match.group(2)
            
            # Skip external URLs
            if img_path.startswith(('http://', 'https://', '//')):
                return f'![{alt_text}]({img_path})'
            
            # Handle Jekyll asset paths
            if img_path.startswith('/'):
                img_path = img_path.lstrip('/')
            
            # Extract just the filename
            img_filename = os.path.basename(img_path)
            
            # Copy the image if it exists
            jekyll_img_path = os.path.join(JEKYLL_DIR, img_path)
            if os.path.exists(jekyll_img_path):
                target_img_path = os.path.join(DOCUSAURUS_ASSETS_DIR, img_filename)
                shutil.copy2(jekyll_img_path, target_img_path)
                print(f"Copied image: {img_filename}")
            else:
                print(f"Warning: Image not found: {jekyll_img_path}")
            
            # Return the updated image reference for Docusaurus
            return f'![{alt_text}](/img/blog/{img_filename})'
        
        return re.sub(img_pattern, replace_img_path, content)
    
    # Process the content
    processed_content = process_image_links(post_content)
    
    # Generate filename for Docusaurus
    # Docusaurus prefers a date prefix for blog posts: YYYY-MM-DD-title.md
    if 'date' in docusaurus_frontmatter:
        date_prefix = docusaurus_frontmatter['date']
    else:
        date_prefix = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Get a file name from the original path or from the title
    if 'slug' in docusaurus_frontmatter:
        file_name = f"{date_prefix}-{docusaurus_frontmatter['slug']}.md"
    else:
        # Fallback to using the original filename or title
        original_filename = os.path.basename(file_path).split('.')[0]
        if original_filename.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            # If the filename already starts with a date, use just the name part
            parts = original_filename.split('-', 3)
            if len(parts) >= 4:
                file_name = f"{date_prefix}-{parts[3]}.md"
            else:
                file_name = f"{date_prefix}-{original_filename}.md"
        else:
            file_name = f"{date_prefix}-{original_filename}.md"
    
    # Remove any special characters from the filename
    file_name = re.sub(r'[^\w.-]', '-', file_name).lower()
    
    # Create the output file
    output_path = os.path.join(DOCUSAURUS_DIR, file_name)
    
    # Generate the Docusaurus file content
    output_content = '---\n'
    output_content += yaml.dump(docusaurus_frontmatter, default_flow_style=False)
    output_content += '---\n\n'
    output_content += processed_content.strip()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"Created Docusaurus post: {output_path}")

if __name__ == "__main__":
    process_jekyll_files()
    print("Conversion completed.")
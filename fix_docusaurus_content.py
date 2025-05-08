import os
import re
import yaml
import json
from pathlib import Path

# Configuration
DOCUSAURUS_BLOG_DIR = os.path.join(os.path.dirname(__file__), 'aks-blog', 'blog')
DOCUSAURUS_AUTHORS_DIR = os.path.join(os.path.dirname(__file__), 'aks-blog', 'blog', 'authors')

def fix_authors_in_frontmatter():
    """Fix author references in blog post frontmatter"""
    print("Fixing author references in blog posts...")
    
    # Get available author IDs from authors directory
    available_authors = {}
    if os.path.exists(DOCUSAURUS_AUTHORS_DIR):
        for author_file in os.listdir(DOCUSAURUS_AUTHORS_DIR):
            if author_file.endswith('.json'):
                author_id = author_file.replace('.json', '')
                author_path = os.path.join(DOCUSAURUS_AUTHORS_DIR, author_file)
                try:
                    with open(author_path, 'r', encoding='utf-8') as f:
                        author_data = json.load(f)
                        # Create a mapping of author name to author ID
                        if 'name' in author_data:
                            available_authors[author_data['name']] = author_id
                except Exception as e:
                    print(f"Error reading author file {author_file}: {e}")
    
    # Find all markdown files in the blog directory
    blog_files = []
    for root, _, files in os.walk(DOCUSAURUS_BLOG_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                blog_files.append(os.path.join(root, file))
    
    print(f"Processing {len(blog_files)} blog files...")
    
    for file_path in blog_files:
        try:
            fix_file_authors(file_path, available_authors)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def fix_file_authors(file_path, available_authors):
    """Fix authors in a single file"""
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
    
    # Fix authors format
    if 'authors' in frontmatter:
        authors = frontmatter['authors']
        
        # Case 1: Authors is a list of strings (names)
        if isinstance(authors, list) and all(isinstance(item, str) for item in authors):
            new_authors = []
            for author_name in authors:
                # Check if we have this author in our mapping
                if author_name in available_authors:
                    new_authors.append(available_authors[author_name])
                else:
                    # Create slug from name
                    author_slug = author_name.lower().replace(" ", "-")
                    new_authors.append(author_slug)
            
            frontmatter['authors'] = new_authors
        
        # Case 2: Authors might already be in correct format - check and ensure
        elif isinstance(authors, list) and all(isinstance(item, str) and not ' ' in item for item in authors):
            # Already looks like author IDs - leave as is
            pass
        
        # Case 3: Single string value
        elif isinstance(authors, str):
            if authors in available_authors:
                frontmatter['authors'] = [available_authors[authors]]
            else:
                author_slug = authors.lower().replace(" ", "-")
                frontmatter['authors'] = [author_slug]
    
    # Fix other common issues
    
    # Fix tags if it's a string instead of a list
    if 'tags' in frontmatter and isinstance(frontmatter['tags'], str):
        frontmatter['tags'] = [tag.strip() for tag in frontmatter['tags'].split(',')]
    
    # Ensure date is in correct format
    if 'date' in frontmatter and isinstance(frontmatter['date'], str):
        # Leave YYYY-MM-DD format as is
        pass
    
    # Generate the updated frontmatter
    updated_frontmatter = yaml.dump(frontmatter, default_flow_style=False)
    
    # Create the updated content
    updated_content = '---\n' + updated_frontmatter + '---\n\n' + post_content
    
    # Write the file back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Fixed authors in {file_path}")

def fix_image_paths():
    """Fix image paths in blog posts"""
    print("Fixing image paths in blog posts...")
    
    blog_files = []
    for root, _, files in os.walk(DOCUSAURUS_BLOG_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                blog_files.append(os.path.join(root, file))
    
    for file_path in blog_files:
        try:
            fix_file_images(file_path)
        except Exception as e:
            print(f"Error fixing images in {file_path}: {e}")

def fix_file_images(file_path):
    """Fix image paths in a single file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern for Markdown image syntax: ![alt text](/path/to/image.jpg)
    img_pattern = r'!\[(.*?)\]\(([^)]+)\)'
    
    def fix_image_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # Skip external URLs and already correct paths
        if img_path.startswith(('http://', 'https://', '//', '/img/')):
            return f'![{alt_text}]({img_path})'
        
        # Handle relative paths
        if not img_path.startswith('/'):
            # Convert relative path to absolute for consistency
            return f'![{alt_text}](/img/blog/{os.path.basename(img_path)})'
        
        # Remove leading slash and adjust path for Docusaurus
        img_path = img_path.lstrip('/')
        return f'![{alt_text}](/img/blog/{os.path.basename(img_path)})'
    
    # Apply the changes
    updated_content = re.sub(img_pattern, fix_image_path, content)
    
    # Only write if changes were made
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Fixed image paths in {file_path}")

def fix_internal_links():
    """Fix internal links in blog posts"""
    print("Fixing internal links in blog posts...")
    
    blog_files = []
    for root, _, files in os.walk(DOCUSAURUS_BLOG_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                blog_files.append(os.path.join(root, file))
    
    for file_path in blog_files:
        try:
            fix_file_links(file_path)
        except Exception as e:
            print(f"Error fixing links in {file_path}: {e}")

def fix_file_links(file_path):
    """Fix internal links in a single file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern for Markdown link syntax: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def fix_link_path(match):
        link_text = match.group(1)
        link_url = match.group(2)
        
        # Skip external URLs and already correct paths
        if link_url.startswith(('http://', 'https://', '//', 'mailto:', '#')):
            return f'[{link_text}]({link_url})'
        
        # Handle Jekyll-style links to internal pages
        if link_url.endswith('.html') or link_url.endswith('.md'):
            # Extract the base name without extension
            base_name = os.path.splitext(os.path.basename(link_url))[0]
            # Convert to Docusaurus blog link format
            return f'[{link_text}](/blog/{base_name})'
        
        return f'[{link_text}]({link_url})'
    
    # Apply the changes
    updated_content = re.sub(link_pattern, fix_link_path, content)
    
    # Only write if changes were made
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Fixed internal links in {file_path}")

def fix_code_blocks():
    """Fix code blocks in blog posts"""
    print("Fixing code blocks in blog posts...")
    
    blog_files = []
    for root, _, files in os.walk(DOCUSAURUS_BLOG_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                blog_files.append(os.path.join(root, file))
    
    for file_path in blog_files:
        try:
            fix_file_code_blocks(file_path)
        except Exception as e:
            print(f"Error fixing code blocks in {file_path}: {e}")

def fix_file_code_blocks(file_path):
    """Fix code blocks in a single file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Convert Jekyll highlighting syntax to standard markdown
    # {% highlight yaml %} -> ```yaml
    content = re.sub(r'{%\s*highlight\s+(\w+)\s*%}', r'```\1', content)
    # {% endhighlight %} -> ```
    content = re.sub(r'{%\s*endhighlight\s*%}', '```', content)
    
    # Write the file back if changes were made
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed code blocks in {file_path}")

if __name__ == "__main__":
    print("Starting to fix transformed Docusaurus content...")
    fix_authors_in_frontmatter()
    fix_image_paths()
    fix_internal_links()
    fix_code_blocks()
    print("Content fixes completed.")
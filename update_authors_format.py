#!/usr/bin/env python3

import os
import re
from pathlib import Path

def update_authors_format(blog_dir):
    """
    Update authors format in Markdown files from list format to array format
    
    Change:
    authors:
    - kenneth-kilty
    
    To:
    authors: [kenneth-kilty]
    """
    print(f"Scanning directory: {blog_dir}")
    
    # Find all Markdown files in the blog directory
    markdown_files = list(Path(blog_dir).glob('*.md'))
    
    if not markdown_files:
        print("No Markdown files found!")
        return
    
    print(f"Found {len(markdown_files)} Markdown files to process")
    
    for md_file in markdown_files:
        with open(md_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Match front matter authors section in list format
        pattern = r'(---\s*[\s\S]*?)(authors:\s*\n-\s*([a-zA-Z0-9_-]+)(?:\s*\n-\s*([a-zA-Z0-9_-]+))*)([\s\S]*?---)'
        
        def replace_authors(match):
            start = match.group(1)
            authors_section = match.group(2)
            end = match.group(5)
            
            # Extract all author IDs
            author_ids = re.findall(r'-\s*([a-zA-Z0-9_-]+)', authors_section)
            
            # Create the new authors line
            if len(author_ids) == 1:
                # For single author, use simpler format
                new_authors_section = f"authors: [{author_ids[0]}]"
            else:
                # For multiple authors, use array format
                new_authors_section = "authors: [" + ", ".join(author_ids) + "]"
            
            return f"{start}{new_authors_section}{end}"
        
        # Apply the replacement
        updated_content = re.sub(pattern, replace_authors, content)
        
        # Only write back if changes were made
        if updated_content != content:
            with open(md_file, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Updated authors format in {md_file}")
        else:
            print(f"No changes needed for {md_file}")

if __name__ == "__main__":
    blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aks-blog", "blog")
    update_authors_format(blog_dir)
    print("Completed processing author formats")
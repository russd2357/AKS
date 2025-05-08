#!/usr/bin/env python3

import os
import re
import yaml

# Input/Output paths
JEKYLL_AUTHORS_PATH = '/home/pina-admin/repos/rdp-AKS/blog-jekyll/_data/authors.yml'
DOCUSAURUS_AUTHORS_PATH = '/home/pina-admin/repos/rdp-AKS/aks-blog/blog/authors.yml'

def convert_authors():
    """Convert Jekyll authors format to Docusaurus authors format"""
    print(f"Reading Jekyll authors from: {JEKYLL_AUTHORS_PATH}")
    
    # Read Jekyll authors file
    with open(JEKYLL_AUTHORS_PATH, 'r', encoding='utf-8') as file:
        jekyll_authors = yaml.safe_load(file)
    
    # Initialize Docusaurus authors dictionary
    docusaurus_authors = {}
    
    # Process each author
    for author_name, author_data in jekyll_authors.items():
        # Create author ID (kebab-case)
        author_id = author_name.lower().replace(' ', '-')
        author_id = re.sub(r'[^a-z0-9-]', '', author_id)
        
        # Create Docusaurus author entry
        author_entry = {
            'name': author_data.get('name', author_name),
            'title': author_data.get('bio', '')
        }
        
        # Add image if available
        if avatar := author_data.get('avatar'):
            if avatar.strip():
                author_entry['image_url'] = avatar
        
        # Process links
        if links := author_data.get('links'):
            # Find best URL for the author
            # Priority: GitHub, LinkedIn, Website/Blog, Twitter/X, Email
            url_priority = {
                'GitHub': 1,
                'Blog': 2,
                'LinkedIn': 3,
                'X': 4,
                'Email': 5
            }
            
            # Sort links by priority
            sorted_links = sorted(links, key=lambda x: url_priority.get(x.get('label', ''), 999))
            
            # Add primary URL
            if sorted_links and 'url' in sorted_links[0]:
                author_entry['url'] = sorted_links[0]['url']
            
            # Add social links
            socials = {}
            for link in links:
                label = link.get('label', '').lower()
                url = link.get('url', '')
                
                if not url:
                    continue
                
                if label == 'x' or label == 'twitter':
                    # Extract username from Twitter/X URL
                    username = url.split('/')[-1]
                    socials['x'] = username
                elif label == 'github':
                    # Extract username from GitHub URL
                    username = url.split('/')[-1]
                    socials['github'] = username
                elif label == 'linkedin':
                    # Extract username from LinkedIn URL
                    username = url.split('/')[-1]
                    socials['linkedin'] = username
                elif label == 'blog' or label == 'website':
                    socials['website'] = url
                elif label == 'email':
                    # Extract email from mailto:
                    if url.startswith('mailto:'):
                        email = url[7:]
                        socials['email'] = email
            
            # Only add socials if we have some
            if socials:
                author_entry['socials'] = socials
        
        # Add to Docusaurus authors
        docusaurus_authors[author_id] = author_entry
    
    # Write Docusaurus authors file
    os.makedirs(os.path.dirname(DOCUSAURUS_AUTHORS_PATH), exist_ok=True)
    with open(DOCUSAURUS_AUTHORS_PATH, 'w', encoding='utf-8') as file:
        yaml.dump(docusaurus_authors, file, default_flow_style=False, sort_keys=False)
    
    print(f"Converted {len(docusaurus_authors)} authors")
    print(f"Docusaurus authors saved to: {DOCUSAURUS_AUTHORS_PATH}")
    
    # Also output a list of author IDs for reference
    print("\nAuthor IDs for reference (use these in your blog posts):")
    for author_id in docusaurus_authors.keys():
        print(f"  - {author_id}")

if __name__ == "__main__":
    convert_authors()
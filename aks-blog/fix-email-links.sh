#!/bin/bash

# Script to fix email links in markdown files
# Azure best practice: All email addresses should use mailto: prefix

echo "Fixing email links in markdown files..."

# Find all markdown files in the blog directory
find ./blog -type f -name "*.md" | while read file; do
  echo "Processing $file"
  
  # Replace plain email addresses with mailto: links
  # This matches email patterns and wraps them in proper markdown mailto links if they aren't already
  sed -i -E 's/([^([]|^)([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})([^)]|$)/\1[\2](mailto:\2)\3/g' "$file"
  
  # Fix any double-wrapped links (in case the script is run multiple times)
  sed -i -E 's/\[\[([^]]+)\]\(mailto:([^)]+)\)\]\(mailto:([^)]+)\)/[\1](mailto:\2)/g' "$file"
done

echo "Email links fixed according to Azure best practices!"

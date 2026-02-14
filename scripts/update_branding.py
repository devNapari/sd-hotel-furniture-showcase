"""
Script to update all templates with new business branding
AM AWUNI FURNITURE & CONSTRUCTION
"""

import os
import re
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Define the replacements
REPLACEMENTS = {
    # Title replacements
    r'SD Hotel Furniture': 'AM AWUNI FURNITURE & CONSTRUCTION',
    r'SD HOTEL FURNITURE': 'AM AWUNI FURNITURE & CONSTRUCTION',
    
    # Brand name in HTML
    r'<span class="brand-sd">SD</span><span class="brand-hotel">HOTEL</span>':
        '<span class="brand-am">AM AWUNI</span><br><span class="brand-furniture">FURNITURE</span> <span class="brand-construction">& CONSTRUCTION</span>',
    
    # Email addresses
    r'contact@sdhotelfurniture\.com': 'amfurnitureandconstruction@gmail.com',
    r'sales@sdhotelfurniture\.com': 'amfurnitureandconstruction@gmail.com',
    r'support@sdhotelfurniture\.com': 'amfurnitureandconstruction@gmail.com',
    r'contact@amawunifurniture\.com': 'amfurnitureandconstruction@gmail.com',
    r'sales@amawunifurniture\.com': 'amfurnitureandconstruction@gmail.com',
    r'support@amawunifurniture\.com': 'amfurnitureandconstruction@gmail.com',
    
    # Address replacements
    r'123 Furniture Avenue': 'Tuutingli, Second Ring Road',
    r'Design City, 12345': 'Near Dabokpa Technical Institute, Tamale',
    r'United States': 'Ghana',
    
    # Phone number replacements
    r'\+1 \(555\) 123-4567': '+233 538 833 723',
    r'\+233 \(0\) 123-456-789': '+233 538 833 723',
    
    # Description
    r'Manufacturing exquisite, durable, and custom-designed furniture for the global hospitality industry\.':
        'Manufacturing quality furniture and providing affordable construction services with eco-friendly materials and flexible payment terms.',
    
    # Categories in footer
    r'Guest Room': 'Sofa Sets',
    r'Lobby & Public Area': 'Dining Tables',
    r'Restaurant & Bar': 'Room Decorations',
    r'Outdoor Furniture': 'Construction Services',
}

def update_file(filepath):
    """Update a single file with new branding"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for pattern, replacement in REPLACEMENTS.items():
            content = re.sub(pattern, replacement, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated: {filepath}")
            return True
        else:
            print(f"[--] No changes: {filepath}")
            return False
    except Exception as e:
        print(f"[ERROR] Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all templates"""
    templates_dir = 'templates'
    updated_count = 0
    
    # Get all HTML files recursively
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_file(filepath):
                    updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Branding update complete!")
    print(f"Updated {updated_count} files")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Quick test to verify the upload path fix
"""

import os
import sys

def test_upload_path():
    print("Testing Upload Path Fix")
    print("=" * 40)
    
    # Check the current directory structure
    upload_dir = "static/uploads/products"
    
    print(f"Upload directory: {upload_dir}")
    
    if os.path.exists(upload_dir):
        files = os.listdir(upload_dir)
        print(f"Files in upload directory: {len(files)}")
        
        # Check for any double-nested directories
        nested_files = [f for f in files if os.path.isdir(os.path.join(upload_dir, f))]
        if nested_files:
            print(f"Nested directories found: {nested_files}")
            for nested in nested_files:
                nested_path = os.path.join(upload_dir, nested)
                if os.path.exists(nested_path):
                    nested_contents = os.listdir(nested_path)
                    print(f"  Contents of '{nested}': {nested_contents}")
        else:
            print("No nested directories found - GOOD!")
            
        # Show some actual files
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        print(f"Image files: {len(image_files)}")
        if image_files:
            print("Sample files:")
            for img in image_files[:3]:
                file_path = os.path.join(upload_dir, img)
                file_size = os.path.getsize(file_path)
                print(f"  - {img} ({file_size} bytes)")
                
    else:
        print(f"Upload directory doesn't exist yet: {upload_dir}")
        
    print("\nThe fix should ensure:")
    print("1. New uploads go directly to: static/uploads/products/")
    print("2. URLs will be: /static/uploads/products/filename.jpg")
    print("3. Shop page can find and display these images")

if __name__ == "__main__":
    test_upload_path()
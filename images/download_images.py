import os
import requests
from PIL import Image
import io
import time
import shutil

# List of images to download with their direct Unsplash URLs
images_to_download = [
    # Breed-specific images
    ("ragdoll-cats-guide.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("bengal-cats-guide.jpg", "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"),
    ("russian-blue-cats-guide.jpg", "https://images.unsplash.com/photo-1513364776144-60967b0f800f"),
    ("maine-coon-cats-guide.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    
    # Toys & Accessories
    ("cat-food-bowls.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-water-bowls.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-collars.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-harnesses.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-furniture.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    
    # Guides & Tips
    ("cat-litter-box.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-travel.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-first-aid.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    
    # Wellbeing
    ("cat-grooming.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
    ("cat-weight-management.jpg", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"),
]

def download_image(url, filename):
    """Download and process an image from a direct URL."""
    try:
        # Add quality parameter to URL
        url = f"{url}?q=80&w=1200&fit=crop"
        
        # Download the image
        response = requests.get(url)
        response.raise_for_status()
        
        # Process the image
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Save the image
        img.save(filename, "JPEG", quality=85)
        print(f"Successfully downloaded and processed {filename}")
        
        # Add a small delay to be respectful to the server
        time.sleep(1)
        
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

def main():
    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
    
    # Move images from subdirectory if they exist
    if os.path.exists("images/images"):
        for filename in os.listdir("images/images"):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                src = os.path.join("images/images", filename)
                dst = os.path.join("images", filename)
                shutil.move(src, dst)
        os.rmdir("images/images")
    
    # Download each image
    for filename, url in images_to_download:
        filepath = os.path.join("images", filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            download_image(url, filepath)
        else:
            print(f"{filename} already exists, skipping...")

if __name__ == "__main__":
    main() 
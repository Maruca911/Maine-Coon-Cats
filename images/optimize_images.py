from PIL import Image
import os

def optimize_image(input_path, output_path, size=(1200, 630), quality=85):
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize image
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            print(f"Optimized: {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

# List of images to optimize
images = [
    'cat-health.jpg',
    'cat-nutrition.jpg',
    'cat-behavior.jpg',
    'cat-care-basics.jpg',
    'cat-anxiety.jpg',
    'cat-dental.jpg',
    'cat-emergency.jpg',
    'cat-supplies.jpg'
]

# Process each image
for image in images:
    if os.path.exists(image):
        optimize_image(image, image)
    else:
        print(f"File not found: {image}") 
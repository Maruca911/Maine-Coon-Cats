import os
import shutil
from pathlib import Path

def build_site():
    # Create public directory if it doesn't exist
    public_dir = Path("public")
    if not public_dir.exists():
        public_dir.mkdir()

    # Copy all HTML files to public directory
    for file in Path(".").glob("*.html"):
        shutil.copy2(file, public_dir / file.name)

    # Copy CSS directory
    css_dir = Path("css")
    if css_dir.exists():
        shutil.copytree(css_dir, public_dir / "css", dirs_exist_ok=True)

    # Copy JS directory
    js_dir = Path("js")
    if js_dir.exists():
        shutil.copytree(js_dir, public_dir / "js", dirs_exist_ok=True)

    # Copy images directory
    images_dir = Path("images")
    if images_dir.exists():
        shutil.copytree(images_dir, public_dir / "images", dirs_exist_ok=True)

    # Copy other necessary files
    for file in ["robots.txt", "sitemap.xml", "manifest.json", "site.webmanifest"]:
        if Path(file).exists():
            shutil.copy2(file, public_dir / file)

    print("Build completed successfully!")

if __name__ == "__main__":
    build_site() 
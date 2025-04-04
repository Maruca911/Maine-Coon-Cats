import os
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "public",
        "css",
        "js",
        "images",
        "blog/guides-and-tips",
        "blog/wellbeing",
        "blog/behavior",
        "blog/breeding",
        "blog/toys-and-accessories",
        "static/images",
        "static/css",
        "static/js"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def copy_files():
    """Copy all necessary files to the public directory"""
    public_dir = Path("public")
    
    # Copy HTML files
    for file in Path(".").glob("*.html"):
        shutil.copy2(file, public_dir / file.name)
    
    # Copy directories
    for directory in ["css", "js", "images"]:
        if Path(directory).exists():
            shutil.copytree(directory, public_dir / directory, dirs_exist_ok=True)
    
    # Copy static files
    for file in ["robots.txt", "sitemap.xml", "manifest.json", "site.webmanifest"]:
        if Path(file).exists():
            shutil.copy2(file, public_dir / file)

def set_permissions():
    """Set proper permissions for all files and directories"""
    for root, dirs, files in os.walk("."):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)
    
    # Make scripts executable
    for script in ["server.py", "build.py"]:
        if Path(script).exists():
            os.chmod(script, 0o755)

def build_site():
    """Main build function"""
    print("Starting build process...")
    
    # Create directories
    print("Creating directories...")
    create_directories()
    
    # Copy files
    print("Copying files...")
    copy_files()
    
    # Set permissions
    print("Setting permissions...")
    set_permissions()
    
    print("Build completed successfully!")

if __name__ == "__main__":
    build_site() 
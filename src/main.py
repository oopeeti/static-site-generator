import os
import shutil
from generation import copy_files_recursively, generate_pages_recursive

PUBLIC_DIR_PATH = "./public"
STATIC_DIR_PATH = "./static"
CONTENT_DIR_PATH = "./content"
TEMPLATE_DIR_PATH = "./template.html"

def main():
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)
    
    print("Copying static files to public directory...")
    copy_files_recursively(STATIC_DIR_PATH, PUBLIC_DIR_PATH)

    print("Generating page...")
    generate_pages_recursive(os.path.join(CONTENT_DIR_PATH), TEMPLATE_DIR_PATH, os.path.join(PUBLIC_DIR_PATH),)

main()

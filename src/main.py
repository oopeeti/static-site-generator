import os
import shutil

PUBLIC_DIR_PATH = "./public"
STATIC_DIR_PATH = "./static"

def copy_directory(source, destination):
    items = os.listdir(source)
    for item in items:
        item_path = os.path.join(source, item)
        dest_item = os.path.join(destination, item)
        print(f"[COPY] {item_path} ---> {dest_item}")
        
        if os.path.isfile(item_path):
            shutil.copy(item_path, os.path.join(destination, item))
        if os.path.isdir(item_path):
            os.mkdir(os.path.join(destination, item))
            
            # Do the function recursively until no more files found
            copy_directory(item_path, dest_item) 
        
def main():
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)
    os.mkdir(PUBLIC_DIR_PATH)
    
    copy_directory(STATIC_DIR_PATH, PUBLIC_DIR_PATH)
main()

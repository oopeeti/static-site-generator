import os, shutil
from markdown_blocks import markdown_to_html_node, extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, item)
        
        # If it's a file, generate an HTML file
        if os.path.isfile(item_path):
            dest_item = os.path.splitext(dest_item)[0] + ".html"
            generate_page(item_path, template_path, dest_item)

        # If its a directory, recurse
        elif os.path.isdir(item_path):
            os.makedirs(dest_item, exist_ok=True)
            generate_pages_recursive(item_path, template_path, dest_item)
        

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Ensure parent folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Read markdown content
    with open(from_path, "r", encoding="utf-8") as markdown_file:
        markdown_content = markdown_file.read()
        
    # Convert markdown to HTML
    title = extract_title(markdown_content)
    html = markdown_to_html_node(markdown_content).to_html()
    
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
            
    new_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Ensure the parent folder of dest_path exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
def copy_files_recursively(source, destination):
    os.makedirs(destination, exist_ok=True)
    
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        dest_item = os.path.join(destination, item)
        print(f"[COPY] {item_path} ---> {dest_item}")
        
        if os.path.isfile(item_path):
            shutil.copy(item_path, os.path.join(destination, item))
        if os.path.isdir(item_path):
            os.mkdir(os.path.join(destination, item))
            
            # Do the function recursively until no more files found
            copy_files_recursively(item_path, dest_item) 
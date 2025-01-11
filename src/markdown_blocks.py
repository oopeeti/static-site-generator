from nodes import HTMLNode
from inline_markdown import *

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in blocks:
        if block == "":
            continue
        
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    elif block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"


markdown = """# My Title

This is a paragraph with *italic* and **bold** text.
It also has a [link to Boot.dev](https://boot.dev) and an
![image of a bear](https://example.com/bear.jpg) in it.

* List item with **bold** text
* List item with *italic* text
* List item with a [link](https://boot.dev)

1. Ordered list element one
2. Ordered list element two
3. Ordered list element three

```This is code block```

[link](https://boot.dev)

> This is a quote with **bold** and *italic* text
"""

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
            html_node = text_node_to_html_node(node)
            html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
        
    return ParentNode("div", children, None)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block.strip("```")
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    list_items = []
    items = block.split("\n")
    for item in items:
        # Remove the * and leading space
        item_text = item[item.find(".")+1:].strip()
        item_children = text_to_children(item_text)
        list_items.append(ParentNode("li", item_children))
    return ParentNode("ol", list_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for item in items:
        # Remove the * and leading space
        item_text = item.lstrip("*").lstrip("-").strip()
        item_children = text_to_children(item_text)
        list_items.append(ParentNode("li", item_children))
    return ParentNode("ul", list_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
        
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def heading_to_html_node(block):
    heading_level = block.count("#")
    
    if(heading_level >= len(block)):
        raise ValueError(f"Invalid heading level: {heading_level}")
    
    # Remove the #s and leading space
    text = block.lstrip("#").strip()
    children = text_to_children(text)
    return ParentNode(f"h{heading_level}", children)
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    elif block_type == "heading":
        return heading_to_html_node(block)
    elif block_type == "code":
        return code_to_html_node(block)
    elif block_type == "ordered_list":
        return olist_to_html_node(block)
    elif block_type == "unordered_list":
        return ulist_to_html_node(block)
    elif block_type == "quote":
        return quote_to_html_node(block)
            
    raise ValueError("Invalid block type")
     
nodes = markdown_to_html_node(markdown)
print(nodes)
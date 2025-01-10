from nodes import *
from inline_markdown import split_nodes_delimiter

def main():
    node1 = TextNode("Normal text ", TextType.TEXT)
    node2 = TextNode("bold text", TextType.BOLD)
    old_nodes = [node1, node2]
    new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)  
    
    
main()

from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url
    
    if text_type not in TextType:
        raise ValueError("Error: Invalid text type detected")

    if text_type == TextType.TEXT:
        return LeafNode(None, text)
    elif text_type == TextType.BOLD:
        return LeafNode("b", text)
    elif text_type == TextType.ITALIC:
        return LeafNode("i", text)
    elif text_type == TextType.CODE:
        return LeafNode("code", text)
    elif text_type == TextType.LINK:
        if(url == None):
            raise ValueError("Error: Can't create Link element without valid href")
        return LeafNode("a", text, {"href": url})        
    elif text_type == TextType.IMAGE:
        if(url == None or text == None):
            raise ValueError("Error: Can't create Image element without valid src and alt")
        return LeafNode("img", "", {"src": url, "alt": text})    

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        

    def __repr__(self):
        return (f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})')
        
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_html = ""
        for key, value in self.props.items():
            html = f' {key}="{value}"'
            props_html += html
            
        return props_html


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            html_props = self.props_to_html()
            if(html_props is not None):
                return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"

    
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        
        if self.children is None:
            raise ValueError("Invalid HTML: no children")

        
        children_html = ""
        
        for child in self.children:
            if child.to_html() is not None:
                children_html += child.to_html()
    
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    

 

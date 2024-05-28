class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        clean_list = []
        for key, value in self.props.items():
            clean_list.append(f'{key}="{value}"')
        return f' {" ".join(clean_list)}'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode needs a value.")
        elif self.tag is None:
            return self.value
        elif self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    ALLOWED_TAGS = {"div", "h1", "h2", "h3", "h4", "h5", "h6", "p",
                    "span", "b", "i", "u", "strong", "em", "img",
                    "a", "ul", "li", "ol", "blockquote", "code", "pre"}

    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            raise ValueError("Children are required for ParentNode.")
        super().__init__(tag, None, children, props=None)

    def to_html(self):
        if self.tag is not None and self.tag not in self.ALLOWED_TAGS:
            raise ValueError(f"Tag '{self.tag}' is not a valid HTML tag.")
        html_text = ""
        for child in self.children:
            html_text += child.to_html()
        return f"<{self.tag}>{html_text}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

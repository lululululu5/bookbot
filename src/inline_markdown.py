import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    delimiters_dict = {
        "**": text_type_bold,
        "*": text_type_italic,
        "`": text_type_code
    }

    for key, value in delimiters_dict.items():
        nodes = split_nodes_delimiter(nodes, key, value)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
            # Reasoning: Once the markdown is closed there will always be a section afterwards. This means that there will be 3 sections if the markdown if opend and closed properly
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_link(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text == "":
            continue

        # This is a tuple with all the matching patterns
        img_tuples = extract_markdown_images(old_node.text)

        if len(img_tuples) == 0:
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            for img_tuple in img_tuples:
                delimiter = f"![{img_tuple[0]}]({img_tuple[1]})"
                # Split only once per image
                parts = current_text.split(delimiter, 1)

                # Part before the delimiter
                if parts[0]:  # If there's text before the image
                    new_nodes.append(TextNode(parts[0], text_type_text))

                # Append the image node
                new_nodes.append(
                    TextNode(img_tuple[0], text_type_image, img_tuple[1]))

                # Update current_text to the remaining part after the delimiter split
                current_text = parts[1]

            if current_text:
                new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text == "":
            continue

        # This is a tuple with all the matching patterns
        link_tuples = extract_markdown_link(old_node.text)

        if len(link_tuples) == 0:
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            for link_tuple in link_tuples:
                delimiter = f"[{link_tuple[0]}]({link_tuple[1]})"
                # Split only once per image
                parts = current_text.split(delimiter, 1)

                # Part before the delimiter
                if parts[0]:  # If there's text before the image
                    new_nodes.append(TextNode(parts[0], text_type_text))

                # Append the image node
                new_nodes.append(
                    TextNode(link_tuple[0], text_type_link, link_tuple[1]))

                # Update current_text to the remaining part after the delimiter split
                current_text = parts[1]

            if current_text:
                new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes

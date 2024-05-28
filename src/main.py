import os
import shutil

from textnode import TextNode
from blocks import markdown_to_html_node


def main():
    generate_pages_recursive("content", "template.html",  "public")


def copy_static(src_path, destination_path):
    # First delete the public directory
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
        print("Public test directory was reset")

    os.mkdir(destination_path)

    def file_generator(src_path, destination_path):

        entries = os.listdir(src_path)
        for entry in entries:
            entry_path = os.path.join(src_path, entry)
            if os.path.isfile(entry_path):
                shutil.copy(entry_path, destination_path)
                print(f"{entry_path} file was copied to {destination_path}")

            else:
                rel_path = os.path.relpath(
                    entry_path, entry_path.split("/")[0])
                temp_path = os.path.join(destination_path, rel_path)
                os.makedirs(temp_path)
                print(f"{temp_path} directory was generated")
                file_generator(entry_path, temp_path)

    file_generator(src_path, destination_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip()[2:]
    raise Exception("Header is necessary.")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r+") as f:
        template = f.read()
    html_title = extract_title(md)
    html_content = markdown_to_html_node(md).to_html()

    temp_template = template.replace("{{ Title }}", html_title).replace(
        "{{ Content }}", html_content)

    with open(dest_path, "w") as f:
        f.write(temp_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.exists("public/majesty"):
        shutil.rmtree("public/majesty")

    os.makedirs(dest_dir_path, exist_ok=True)

    entries = os.listdir(dir_path_content)
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(entry_path) and entry.endswith(".md"):
            with open(entry_path, "r") as f:
                md = f.read()
            with open(template_path, "r") as f:
                template = f.read()

            html_title = extract_title(md)
            html_content = markdown_to_html_node(md).to_html()

            temp_template = template.replace("{{ Title }}", html_title).replace(
                "{{ Content }}", html_content)

            rel_path = os.path.relpath(entry_path, dir_path_content)
            destination_path = os.path.join(
                dest_dir_path, rel_path).replace(".md", ".html")
            destination_dir = os.path.dirname(destination_path)

            os.makedirs(destination_dir, exist_ok=True)

            with open(destination_path, "w") as f:
                f.write(temp_template)

        elif os.path.isdir(entry_path):
            rel_path = os.path.relpath(entry_path, dir_path_content)
            temp_path = os.path.join(dest_dir_path, rel_path)

            os.makedirs(temp_path, exist_ok=True)

            generate_pages_recursive(entry_path, template_path, temp_path)


main()

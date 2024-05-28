import os
import shutil

from textnode import TextNode
from blocks import markdown_to_html_node


def main():
    copy_static(src_path="static",
                destination_path="public")


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
    # Use html_template and fill in the title and the content
    temp_template = template.replace("{{ Title }}", html_title).replace(
        "{{ Content }}", html_content)
    # print(temp_template)

    # copy file to public/index.html
    if os.path.exists(dest_path):
        print("File already exists")
        with open(dest_path, "w") as f:
            f.write(temp_template)
    else:
        print("I'm clearly forgetting something")
        # new_dict = os.makedirs(os.path.dirname(dest_path))
        # new_path = os.path.join(dest_path, "index.html")
        with open(dest_path, "w") as f:
            f.write(temp_template)


generate_page("content/index.md", "template.html", "public/index.html")

# main()

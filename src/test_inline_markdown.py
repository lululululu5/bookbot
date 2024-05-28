import unittest

from textnode import (TextNode, text_type_text, text_type_bold,
                      text_type_italic, text_type_code, text_type_link, text_type_image)

from inline_markdown import (extract_markdown_link, extract_markdown_images,
                             split_nodes_image, split_nodes_link, text_to_textnodes, split_nodes_delimiter)


class TestInlineMarkdown(unittest.TestCase):
    def test_eq_textnodegen_code(self):
        node = TextNode(
            "This is text with a `code block` word", text_type_text)
        input = split_nodes_delimiter(
            [node], delimiter="`", text_type=text_type_code)
        self.assertEqual([
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ], input
        )

    def test_eq_textnodegen_bold(self):
        node = TextNode(
            "This is text with a **bold** word", text_type_text)
        input = split_nodes_delimiter(
            [node], delimiter="**", text_type=text_type_bold)
        self.assertEqual([
            TextNode("This is text with a ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word", text_type_text),
        ], input
        )

    def test_eq_textnodegen_italic(self):
        node = TextNode(
            "This is text with a *italic* word and this is another *italic* word", text_type_text)
        input = split_nodes_delimiter(
            [node], delimiter="*", text_type=text_type_italic)
        self.assertEqual([
            TextNode("This is text with a ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and this is another ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word", text_type_text),
        ], input
        )

    def test_eq_textnodegen_first(self):
        node = TextNode(
            "*Italic* text", text_type_text
        )
        input = split_nodes_delimiter(
            [node], delimiter="*", text_type=text_type_italic)
        self.assertEqual([TextNode("Italic", text_type_italic),
                          TextNode(" text", text_type_text)], input)

    def test_eq_textnodegen_last(self):
        node = TextNode(
            "This text is *italic*", text_type_text
        )
        input = split_nodes_delimiter(
            [node], delimiter="*", text_type=text_type_italic)
        self.assertEqual([TextNode("This text is ", text_type_text),
                          TextNode("italic", text_type_italic)], input)

    def test_eq_regex_img(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
                         )

    def test_eq_regex_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_link(text)
        self.assertEqual(result, [("link", "https://www.example.com"),
                         ("another", "https://www.example.com/another")])

    def test_eq_img_to_textnode(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ])

    def test_eq_link_to_textnode(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link,
                     "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode(
                "another", text_type_link, "https://www.example.com/another"
            ),
        ])

    def test_eq_text_to_textnodes(self):
        result = (text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"))
        self.assertEqual(result, [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        )


if __name__ == "__main__":
    unittest.main()

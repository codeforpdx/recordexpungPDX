import markdown2
import pdfkit
import requests
import pathlib
from os import path


class MarkdownToPDF:
    @staticmethod
    def to_pdf(title: str, markdown_source: str) -> bytes:
        html_style = MarkdownToPDF.css()
        html_body = markdown2.markdown(markdown_source, extras=["tables"])
 
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <style>
                {html_style}
            </style>
        </head>
        <body class="markdown-body">
            {html_body}
        </body>
        </html>
        """
        return pdfkit.from_string(html, False, options={"quiet": ""})

    @staticmethod
     # Reads 'style.txt' to string. 
     ## 'style.txt' copied from https://raw.githubusercontent.com/sindresorhus/github-markdown-css/gh-pages/github-markdown.css
    def css():
        fp = path.join(pathlib.Path(__file__).parent, "style.txt")
      
        with open(fp, 'r') as f:
            text = f.read()

        return text


if __name__ == "__main__":
    MarkdownToPDF.to_pdf("Test title", "# Test Header")

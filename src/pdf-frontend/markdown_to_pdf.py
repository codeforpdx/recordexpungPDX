import markdown2
import pdfkit
import requests


class MarkdownToPDF:
    @staticmethod
    def to_pdf(filename, title, source):
        html_style = MarkdownToPDF.css()
        html_body = markdown2.markdown(source)
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
        pdfkit.from_string(html, filename)

    @staticmethod
    def css():
        response = requests.get(
            "https://raw.githubusercontent.com/sindresorhus/github-markdown-css/gh-pages/github-markdown.css"
        )
        return response.text

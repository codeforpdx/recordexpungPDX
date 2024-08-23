import markdown2
import pdfkit
import requests


class MarkdownToPDF:
    @staticmethod
    def to_pdf(title: str, markdown_source: str) -> bytes:
        html_style = MarkdownToPDF.css()
        html_body = markdown2.markdown(markdown_source)
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
    def css():
        response = requests.get(
            "https://raw.githubusercontent.com/sindresorhus/github-markdown-css/gh-pages/github-markdown.css"
        )

        return response.text


if __name__ == "__main__":
    MarkdownToPDF.to_pdf("Test title", "# Test Header")

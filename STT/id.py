from bs4 import BeautifulSoup
import re

class CallerNumberExtractor:
    def __init__(self, html_file_path: str):
        self.html_file_path = html_file_path
        self.text = ""

    def load_and_clean_html(self):
        with open(self.html_file_path, "r", encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        self.text = soup.get_text(separator='\n', strip=True)

    def extract_caller_number(self) -> str | None:

        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Номер вызывающего абонента" in line:
                if i + 1 < len(lines):
                    number_line = lines[i + 1]
                    number = re.sub(r'\D', '', number_line)
                    return number
        return None

# extractor = CallerNumberExtractor("cdr_description1.html")
# extractor.load_and_clean_html()
# caller_number = extractor.extract_caller_number()
# print(caller_number)









import sys, re
import htmlgenerator as hg

class MarkdownTagService():
    header_tag_regex = re.compile(r'^#{1,6}\s')
    link_tag_regex = ''

class GenerateHtmlService():
    """Services to convert content into HTML Tags"""

    def create_header(self, size: int, content: str) -> str:
        """Converts the Content into Header Tags based on the size"""
        return f'<h{size}>{content}</h{header_size}>'

if __name__ == '__main__':

    file_name : str = sys.argv[1]
    markdown_service : MarkdownTagService = MarkdownTagService()
    generate_html_service : GenerateHtmlService = GenerateHtmlService()

    html_elements = []
    with open(file_name, encoding="utf-8") as file:
        
        for line in file:

            #Find if the line begins with a header
            header_search : re.Match[str] = markdown_service.header_tag_regex.search(line)

            if header_search is not None:
                #Create HTML Header tag based on size of #, strip off whitespace
                header_size: int = len(header_search.group(0).strip())

                # Remove the newline at the end of header and the # signs at the beginning of the line.
                # Header text should all exist on #Same line for compatibility
                # Reference: https://www.markdownguide.org/basic-syntax/
                formatted_line: str = markdown_service.header_tag_regex.sub('', line.strip())

                print(generate_html_service.create_header(header_size, formatted_line))
            else:
                #created formatted p tags around entire string until \n in next line
                print(line, end='')
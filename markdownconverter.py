import sys, re

class MarkdownTagService():
    header_tag_regex = re.compile(r'^#{1,6}\s')
    link_tag_regex = re.compile(r'\[[^\]]*\]\([^\)]*\)')
    link_text_regex = re.compile(r'\[([^\]]*)\]')
    href_text_regex = re.compile(r'\(([^)]*)\)')

class GenerateHtmlService():
    """Services to convert content into HTML Tags"""

    __Markdown: MarkdownTagService

    def __init__(self):
        self.__Markdown = MarkdownTagService

    def create_header(self, size: int, content: str) -> str:
        """Converts the Content into Header Tags based on the size"""
        return f'<h{size}>{content}</h{size}>'

    def create_unformatted_text( self, content: str) -> str:
        """Converts the content into unformatted text surrounded by p tags"""
        return f'<p>{content}</p>'

    def create_anchor_tag( self, content) -> str:
        """Creates Anchor tags for each Markdown Link"""
        link_text_search: re.Match[str] = self.__Markdown.link_text_regex.search(content)
        href_text_search: re.Match[str] = self.__Markdown.href_text_regex.search(content)
        link_text: str = ''
        href_text: str = ''
        
        if link_text_search is not None:
            link_text = link_text_search.group(0).strip('[]')
        
        if href_text_search is not None:
            href_text = href_text_search.group(0).strip('()')

        return f'<a href=\'{href_text}\'>{link_text}</a>'

if __name__ == '__main__':

    file_name : str = sys.argv[1]
    Markdown : MarkdownTagService = MarkdownTagService()
    GenerateHtml : GenerateHtmlService = GenerateHtmlService()

    with open(file_name, encoding="utf-8") as file:

        unformatted_line: str = ''

        for line in file:

            #Find if the line begins with a header
            header_search : re.Match[str] = Markdown.header_tag_regex.search(line)

            # if the line is a newline and no unformatted_line_text has been recorded
            # print out the recorded unformatted_line_text and empty it out
            if line == '\n' and unformatted_line != '':
                print(GenerateHtml.create_unformatted_text(unformatted_line.strip()))
                unformatted_line = ''

            if header_search is not None:
                #Create HTML Header tag based on size of #, strip off whitespace
                header_size: int = len(header_search.group(0).strip())

                # Remove the newline at the end of header and the # signs at the beginning of the line.
                # Header text should all exist on #Same line for compatibility
                # Reference: https://www.markdownguide.org/basic-syntax/
                formatted_line: str = Markdown.header_tag_regex.sub('', line.strip())

                link_search_matches = Markdown.link_tag_regex.finditer(formatted_line)
                
                if link_search_matches is not None:
                    
                    # replace each matched instance with the anchor tag
                    for link_search_match in link_search_matches:
                     
                        anchor_tag = GenerateHtml.create_anchor_tag(formatted_line)
                        link_search_match_text = link_search_match.group(0)

                        formatted_line = formatted_line.replace( link_search_match_text, anchor_tag, 1)

                print(GenerateHtml.create_header(header_size, formatted_line))
            elif line != '\n':
                #add lines together that are not newlines to put into <p> tags
                unformatted_line += line
            else:
                print(line.strip())

        #print out any remaining lines that might have been recorded
        if unformatted_line != '':
            print(GenerateHtml.create_unformatted_text(unformatted_line), end='')

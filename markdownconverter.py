"""Coding Exercise"""
import sys
import re

class MarkdownTagService():
    """Class Containing supported regular expressions for tags in markdown"""
    header_tag_regex = re.compile(r'^#{1,6}\s')
    link_tag_regex = re.compile(r'\[([^\]]*\]?)\]\([^\)]*\)')

class GenerateHtmlService():
    """Services to convert content into HTML Tags"""

    __link_text_regex = re.compile(r'\[([^\]]*\]?)\]')
    __href_text_regex = re.compile(r'\(([^)]*)\)')
    __Markdown: MarkdownTagService

    def __init__(self) -> None:
        self.__Markdown = MarkdownTagService()

    def create_header(self, size: int, content: str) -> str:
        """Converts the Content into Header Tags based on the size"""
        return f'<h{size}>{content}</h{size}>'

    def create_unformatted_text( self, content: str) -> str:
        """Converts the content into unformatted text surrounded by p tags"""
        return f'<p>{content}</p>'

    def create_anchor_tag( self, content: str) -> str:
        """Creates Anchor tags for each Markdown Link"""
        link_text_search: re.Match[str] = self.__link_text_regex.search(content)
        href_text_search: re.Match[str] = self.__href_text_regex.search(content)
        link_text: str = ''
        href_text: str = ''

        if link_text_search is not None:
            link_text = link_text_search.group(0)[1:-1]

        if href_text_search is not None:
            href_text = href_text_search.group(0).strip('()')

        return f'<a href=\'{href_text}\'>{link_text}</a>'

    def replace_header_tag_in_markdown_text( self, markdown_line: str) -> str:
        """Method to replace markdown text with html header tags"""

        header_search: re.Match[str] = Markdown.header_tag_regex.search(markdown_line)
        altered_html: str = markdown_line

        #Create HTML Header tag based on size of #, strip off whitespace
        header_size: int = len(header_search.group(0).strip())
        altered_html = self.__Markdown.header_tag_regex.sub('', markdown_line.strip())

        return self.create_header(header_size, altered_html)

    def replace_anchor_tag_in_markdown_text( self, markdown_line: str) -> str:
        """Method to replace markdown text with html anchor tags"""

        link_search_matches = self.__Markdown.link_tag_regex.finditer(markdown_line)
        altered_html: str = markdown_line
        if link_search_matches is not None:

            # replace each matched instance with the anchor tag
            for link_search_match in link_search_matches:

                anchor_tag = self.create_anchor_tag(altered_html)
                link_search_match_text = link_search_match.group(0)

                altered_html = altered_html.replace( link_search_match_text, \
                                    anchor_tag, 1)

        return altered_html

if __name__ == '__main__':

    file_name : str = sys.argv[1]
    Markdown : MarkdownTagService = MarkdownTagService()
    GenerateHtml : GenerateHtmlService = GenerateHtmlService()

    with open(file_name, encoding="utf-8") as file:

        unformatted_line_block: str = ''

        for line in file:

            #Find if the line begins with a header
            header_search : re.Match[str] = Markdown.header_tag_regex.search(line)

            # if the line is a newline and no unformatted_line_text has been recorded
            # print out the recorded unformatted_line_text and empty it out
            if line == '\n' and unformatted_line_block != '':
                print(GenerateHtml.create_unformatted_text(unformatted_line_block.strip()))
                unformatted_line_block = ''

            if header_search is not None:

                # Remove the newline at the end of header and the # signs at the
                # beginning of the line. Header text should all exist on
                # Same line for compatibility
                # Reference: https://www.markdownguide.org/basic-syntax/
                formatted_line: str = GenerateHtml.replace_header_tag_in_markdown_text(line)
                formatted_line = GenerateHtml.replace_anchor_tag_in_markdown_text(formatted_line)

                print(formatted_line)
            elif line != '\n':
                #add lines together that are not newlines to put into <p> tags
                formatted_line: str = GenerateHtml.replace_anchor_tag_in_markdown_text(line)

                unformatted_line_block += formatted_line
            else:
                print(line.strip())

        #print out any remaining lines that might have been recorded
        if unformatted_line_block != '':
            print(GenerateHtml.create_unformatted_text(unformatted_line_block), end='')

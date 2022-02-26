# Import Module
from bs4 import BeautifulSoup

# HTML Document
HTML_DOC = """
              <html>
                <head>
                    <title> Geeksforgeeks </title>
                    <style>.call {background-color:black;} </style>
                    <script>getit</script>
                </head>
                <body>
                    is a
                    <div>Computer Science portal.</div>
                </body>
              </html>
            """


# Function to remove tags
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['head', 'script']):
        # Remove tags
        # data.decompose()
        data.clear()

    # return data by retrieving the tag content
    # return ' '.join(soup.stripped_strings)
    return soup

# Print the extracted data
print(remove_tags(HTML_DOC))

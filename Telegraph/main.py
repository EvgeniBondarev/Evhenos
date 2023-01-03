from my_telethon import Telegraph
import re
from bs4 import BeautifulSoup
import telegraph


def main():
    '[{"tag":"p", "children":["Hello, world!"]},{"tag":"a", "attrs":{"href":"https://api.telegra.ph/"}, "children":["link"]}]' 
  
    BLOCK_ELEMENTS = {
    'address', 'article', 'aside', 'blockquote', 'canvas', 'dd', 'div', 'dl',
    'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav',
    'noscript', 'ol', 'output', 'p', 'pre', 'section', 'table', 'tfoot', 'ul',
    'video'
    }
    
 
    with open("index.html", "r") as f:
    
        contents = f.read()
    
        soup = BeautifulSoup(contents, 'lxml')
    
        print(soup.find_all())
  
     
if __name__ == "__main__":
    main()
    
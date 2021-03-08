from lxml import etree
import re, sys
from utils import stringify_children, remove_stoplist_lines

invalid_pages=set(["photo-stories","recipes","bollywood","slideshow","relationships","bollywood-unknown_photo-stories","cartoon","Weather","Cartoonscape","cartoonscape", "Bullion-Rates", "Exchange-Rates"])
stoplist = ["ShareArticle","Updated:","MoreIn","SpecialCorrespondent","METRO PLUS","EDUCATION PLUS","PROPERTY PLUS","CINEMA PLUS","DISTRICT PLUS", "Share Via Email"]

if __name__ == "__main__":
    filename = sys.argv[1]

    if set.intersection(set(filename.split("_")), invalid_pages):
        print("Filename in pass_list: " + filename)
        sys.exit(0)

    with open("tmp/htmls/" + filename, "rb") as f:
        html_string = f.read()

    htmlparser = etree.HTMLParser(remove_comments=True)
    doc = etree.HTML(html_string, htmlparser)
    if doc is None:
        print("Couldn't load html: " + filename)
        sys.exit(0)

    node=doc.xpath('//div[contains(@id,"content-body")]')
    if not node:
        node =doc.xpath('//div/p')
    if not node:
        node =doc.xpath('//p')
    if node:
        text="".join([stringify_children(x) for x in node])
    else:
        print("Can't extract text: ", filename)
        sys.exit(0)

    text = remove_stoplist_lines(text, stoplist)
    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit(0)

    # Add title
    title = " ".join(doc.xpath("//h1//text()")).lstrip("\n").split("\n")[0]
    text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

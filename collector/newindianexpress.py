from lxml import etree
import re, sys
from utils import stringify_children

if __name__ == "__main__":
    filename = sys.argv[1]

    with open("tmp/htmls/" + filename, "rb") as f:
        html_string = f.read()

    htmlparser = etree.HTMLParser(remove_comments=True)
    doc = etree.HTML(html_string, htmlparser)
    if doc is None:
        print("Couldn't load html: " + filename)
        sys.exit(0)

    #node = doc.xpath('//div[contains(@class, "article")]')
    node =doc.xpath('//div[contains(@id,"content")]')
    if node:
        lines="".join([stringify_children(x) for x in node]).split("\n")
    if not node :
        print("Can't extract text: ", filename)
        sys.exit(0)

    if "Share Via Email" in lines:
        lines.remove("Share Via Email")

    text = "\n".join([line for line in lines if re.search("\S", line)])

    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit(0)

    # Add title
    title = " ".join(doc.xpath("//h1//text()")).lstrip("\n").split("\n")[0]
    text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

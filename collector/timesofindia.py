from lxml import etree
import re, sys
from utils import stringify_children, remove_all_lines_after_stoplist

stoplist = ["RELATED", "From around the web", "More from The Times of India", "Recommended By Colombia",
            "more from times of india Cities","You might also", "You might also like", "more from times of india",
            "All Comments ()+^ Back to Top","more from times of india News","more from times of india TV",
            "more from times of india Sports","more from times of india Entertainment","more from times of india Life & Style",
            "more from times of india Business", "... contd.", "Please read our terms of use before posting comments"]
stoplist2 = ["FOLLOW US","FOLLOW PHOTOS","FOLLOW LIFE & STYLE"]

invalid_pages=set(["photo-stories","recipes","bollywood","slideshow","relationships","bollywood-unknown_photo-stories"])

if __name__ == "__main__":
    filename = sys.argv[1]

    if set.intersection(set(filename.split("_")), invalid_pages):
        print("Filename in pass_list: " + filename)
        sys.exit(0)

    with open(filename, "rb") as f:
        html_string = f.read()

    htmlparser = etree.HTMLParser(remove_comments=True)
    doc = etree.HTML(html_string, htmlparser)
    if not doc:
        print("Couldn't load html: " + filename)
        sys.exit(0)

    node = doc.xpath('//div[contains(@class, "Normal")]')
    if node:
        text = ""
        for s in [re.sub(r" {2,}|\n|\t|\r", r"", x) for x in doc.xpath('//div[contains(@class, "Normal")]/text()')]:
            if s:
                text += s
                break
        text += stringify_children(node[0])
    else:
        node = doc.xpath('//div[@class="txt"]')
        if node:
            text = stringify_children(node[0])
        else:
            text = "".join(doc.itertext(tag="p"))
            if not text:
                print("Can't extract text: ", filename)
                sys.exit(0)

    # Clean
    text = remove_all_lines_after_stoplist(text, stoplist)
    text = remove_stoplist_lines(text, stoplist2)
    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit(0)

    # Add title
    title = " ".join(doc.xpath("//h1/text()"))
    text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

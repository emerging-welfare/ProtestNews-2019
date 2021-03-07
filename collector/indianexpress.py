from lxml import etree
import re, sys
from utils import stringify_children, remove_all_lines_after_stoplist

stoplist = ["Tags:","ALSO READ","Please read our before posting comments","TERMS OF USE: The views expressed in comments published on indianexpress.com are those of the comment writer's alone. They do not represent the views or opinions of The Indian Express Group or its staff. Comments are automatically posted live; however, indianexpress.com reserves the right to take it down at any time. We also reserve the right not to publish comments that are abusive, obscene, inflammatory, derogatory or defamatory.", "... contd.", "Please read our terms of use before posting comments"]

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "rb") as f:
        html_string = f.read()

    htmlparser = etree.HTMLParser(remove_comments=True)
    doc = etree.HTML(html_string, htmlparser)
    if not doc:
        print("Couldn't load html: " + filename)
        sys.exit(0)

    node = doc.xpath('//div[contains(@class, "contentstory")]')
    if node:
        text = ""
        for s in [re.sub(r" {2,}|\n|\t|\r", r"", x) for x in doc.xpath('//div[contains(@class, "contentstory")]/text()')]:
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

    text = remove_all_lines_after_stoplist(text, stoplist)
    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit(0)

    # Add title
    title = doc.xpath("//title/text()")
    title = "".join([i for i in title])
    if title:
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

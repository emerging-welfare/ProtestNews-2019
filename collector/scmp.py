from lxml import etree
import re,sys
from utils import remove_all_lines_after_stoplist, remove_stoplist_lines

stoplist = ["Print Email","Video"]
stoplist2 = ["Viewed","Associated Press","Get updates direct to your inbox","Opinion"]

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r",encoding="utf-8") as f:
        html_string = f.read()

    htmlparser = etree.HTMLParser(remove_comments=True)
    doc = etree.HTML(html_string, htmlparser)
    if not doc:
        print("Couldn't load html: " + filename)
        sys.exit(0)

    text=" ".join([x for x in doc.xpath('//div//p/text()') if not x.lower().startswith("you are signed")])

    # Clean
    text = remove_all_lines_after_stoplist(text, stoplist)
    text = remove_stoplist_lines(text, stoplist2)
    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit(0)

    # Add title
    title = " ".join(doc.xpath('//h1/text()'))
    text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

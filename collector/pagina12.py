from lxml import etree
import re,sys

PATTERN_1 = re.compile(r'ar_[0-9]+_[0-9]+-[0-9]+_[0-9]+-[0-9]+-[0-9]+_pa')
PATTERN_2 = re.compile(r'ar_[0-9]+-[\w-]+[\w]')
PATTERN_3 = re.compile(r'ar_[A-Za-z-]+')

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, "rb") as f:
        htmltext = f.read()

    htmlparser = etree.HTMLParser()
    tree = etree.HTML(htmltext, htmlparser)

    text, title = "", ""
    if PATTERN_1.search(filename):
        text = "".join(tree.xpath("//table//text()"))
    elif PATTERN_2.search(filename):
        text = "".join(tree.xpath("//div[@class=\"article-text\"]//text()"))
        title = "".join(tree.xpath("//div[@class=\"article-title\"]//text()"))
    elif PATTERN_3.search(filename):
        text = "".join(tree.xpath("//div[@id=\"cuerpo\"]//text()"))
        title = "".join(tree.xpath("//div[@class=\"nota top12\"]/h2/text()"))

    if not text.strip():
        print("Can't extract text: ", filename)
        sys.exit(0)

    if title.strip():
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

from lxml import etree
import re,sys
from utils import remove_stoplist_lines

stoplist = ['Email | Print', '+', 'stumbleupon', 'More Pictures', 'Save Article', 'Click the "PLAY" button and listen. Do you like the online audio service here?','Good, I like it','Do you have anything to say?','Name']

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r",encoding="utf-8") as f:
        html_string = f.read()

    htmlparser = etree.HTMLParser(remove_comments=True)
    doc = etree.HTML(html_string, htmlparser)
    if not doc:
        print("Couldn't load html: " + filename)
        sys.exit(0)

    title=" ".join(doc.xpath('//table//div[@id="p_title"]/text()'))
    if not title:
        title= " ".join(doc.xpath('//*//h1//text()'))
    if not title:
        title= doc.xpath('//*//h2//text()')[0] if doc.xpath('//*//h2//text()') else ""
        if title:
            text=" ".join([x.strip("\n \t") for x in doc.xpath('//*//p//text()')]).strip()

    if not text:
        text=" ".join([x.strip() for x in doc.xpath('//table//*//div[@id="p_content"]//text()')[:-1]]).strip("[ ]")
    if not text:
        text=" ".join([x.strip() for x in doc.xpath('//*[@id="p_content"]//text()')[:-1]])
    if not text:
        text=" ".join([x.strip() for x in doc.xpath('*//div[@id="ivs_content"]/text()')]).strip("\n ")
    if not text:
        text=" ".join([x.strip("\n\t ") for x in doc.xpath('*//p/text()') if x.strip("\n\t |")])
    if not text.strip():
        print("Can't extract text: ", filename)
        sys.exit()

    # Clean
    text = remove_stoplist_lines(text, stoplist)
    text = "\n".join([line for line in text.splitlines() if not line.startswith('Source')])
    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit()

    if title:
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

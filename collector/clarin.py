from lxml import etree
import re,sys

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, "r") as f:
        htmltext = f.read()

    htmlparser = etree.HTMLParser()
    tree = etree.HTML(htmltext, htmlparser)

    # extract info from html file
    text = ' '.join(tree.xpath('//div[@itemprop="description"]//text()') + \
                    [etree.tostring(element, encoding="unicode", method="text") \
                     for element in tree.xpath('//*[@class="body-nota"]/*') \
                     if element.tag in ("p", "h1", "h2", "h3", "h4", "h4", "h5", "h6")])
    text = re.sub(r"\s+", " ", text).strip()

    title = ' '.join(tree.xpath('//h1[@id="title"]//text()'))

    if len(text) < 10:
        print("Can't extract text: ", filename)
        sys.exit(0)

    if title.strip():
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

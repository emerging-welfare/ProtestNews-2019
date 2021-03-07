from lxml import etree
import re,sys

PASS_LIST = ['agenda-cultural', 'https___suscripciones']

if __name__ == '__main__':
    filename = sys.argv[1]

    if any(x in filename for x in PASS_LIST):
        print("Filename in pass list: ", filename)
        sys.exit(0)

    with open(filename, "r") as f:
        htmltext = f.read()

    htmlparser = etree.HTMLParser()
    tree = etree.HTML(htmltext, htmlparser)

    # extract info from html file
    text = ' '.join(etree.tostring(element, encoding="unicode", method="text") \
                    for element in tree.xpath('//*[@id="cuerpo"]/*') \
                    if element.tag in ("p", "h1", "h2", "h3", "h4", "h4", "h5", "h6"))
    text = re.sub(r"\s+", " ", text).strip()

    title = ' '.join(tree.xpath('//h1[@class="titulo"]//text()'))

    if not text.strip():
        print("Can't extract text: ", filename)
        sys.exit(0)

    if title.strip():
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

from lxml import etree
import re,sys

PASS_LIST = ["___esportefera.com.br", "br_galerias_", "br_fotos", ".DS_Store", "emais.estadao.com.br", "jornaldocarro.estadao.com.br", "___tv.estadao"]

if __name__ == '__main__':
    filename = sys.argv[1]

    if any(x in filename for x in PASS_LIST):
        print("Filename in pass list: ", filename)
        sys.exit(0)

    with open("tmp/htmls/" + filename, "r") as f:
        htmltext = f.read()

    htmlparser = etree.HTMLParser()
    tree = etree.HTML(re.sub('(<!--.*?-->)', ' ', htmltext), htmlparser)

    title, text = "", ""

    # extract info from html file
    if "noticia__state" in htmltext:
        if 'class="n--noticia__subtitle"' in htmltext:
            text += ' '.join(tree.xpath('//*[@class="n--noticia__subtitle"]//text()')).replace('\n', '')
        if 'class="n--noticia__content content"' in htmltext:
            text += "\n" + ' '.join(tree.xpath('//*[@class="n--noticia__content content"]/p/text()')).replace('\n', '')
            if text == "\n":
                text += ' '.join(tree.xpath('//*[@class="n--noticia__content content"]/p/span/text()')).replace('\n', '')

        title = ' '.join(tree.xpath('//*[@class="n--noticia__title"]//text()')).replace('\n', '')

    elif "h1 class=\"title\"" in htmltext:
        text = ' '.join(tree.xpath('//*[@class="content-text content"]/p/text()')).replace('\n', '')
        title = ' '.join(tree.xpath('//*[@class="thumb-tit"]//text()')).replace('\n', '')
    else:
        print("Can't extract text: ", filename)
        sys.exit(0)

    text = re.sub(r"Veja também: '[^']*'", "\n", text)

    if not text.strip():
        print("No text after cleanup: ", filename)
        sys.exit(0)

    if title.strip():
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

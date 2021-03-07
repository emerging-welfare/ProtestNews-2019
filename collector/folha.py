from lxml import etree
import re,sys

reg = re.compile("location.replace\(\s*\"http\:\/\/www1\.folha\.uol\.com\.br\/.*\"\s*\)\s*;")  # matching
rep = re.compile("location.replace\(\s*\"|\"\s*\)\s*;") # replace

PASS_LIST = ['indicadores', ]

# def url_to_filename(url):
#     return url.replace('://', '___').replace('/', '_')

if __name__ == '__main__':
    filename = sys.argv[1]

    if any(x in filename for x in PASS_LIST):
        print("Filename in pass list: ", filename)
        sys.exit(0)

    with open(filename, "r", encoding="ISO-8859-1") as f:
        htmltext = f.read()

    htmlparser = etree.HTMLParser()
    tree = etree.HTML(re.sub('(<!--.*?-->)', ' ', htmltext), htmlparser)

    title, text = "", ""

    # files that have link redirection
    redirection_links = re.findall(reg, htmltext)
    if len(redirection_links) != 0:
        # redirected_files.append((filename, url_to_filename(re.sub(rep, "", redirection_links[0]))))
        print("Redirection link: " + filename)
        sys.exit(0)

    # extract info from html file
    elif 'id="articleNew"' in htmltext:
        text = ' '.join(tree.xpath('//*[@id="articleNew"]/p//text()')).replace('\n', '')
        title = ' '.join(tree.xpath('//*[@id="articleNew"]/h1//text()')).replace('\n', '')

    elif 'class="article"' in htmltext:
        text = ' '.join(tree.xpath('//*[@class="article"]')[0].itertext()).replace('\n', '')
        title = ' '.join(tree.xpath('//*[@class="article"]/h1//text()')).replace('\n', '')

    elif 'itemprop="articleBody"' in htmltext:
        text = ' '.join(tree.xpath('//*[@itemprop="articleBody"]/p//text()')).replace('\n', '')
        title = ' '.join(tree.xpath('//*[@itemprop="headline"]/text()')).replace('\n', '')

    elif 'name="conteudo"' in htmltext:
        text = ' '.join(tree.xpath('//article/div/p//text()')).replace('\n', '')
        title = ' '.join(tree.xpath('//article/header/h1//text()')).replace('\n', '')

    else:
        print("Can't extract text: ", filename)
        sys.exit(0)

    if not text.strip():
        print("Can't extract text: ", filename)
        sys.exit(0)

    if title.strip():
        text = title + "\n" + text

    with open("tmp/texts/" + filename, "w", encoding="utf-8") as g:
        g.write(text)

    print("Finished html-to-text: " + filename)

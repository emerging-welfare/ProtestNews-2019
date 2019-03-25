import sys
import lxml.html

filename = sys.argv[1]

with open("tmp/texts/" + filename, "r", encoding="utf-8") as f:
    text = f.read().splitlines()

with open("tmp/htmls/" + filename, "rb") as g:
    html_string = g.read()

def addnewstime(lines, html_string):

    doc = lxml.html.document_fromstring(html_string)
    title = doc.xpath("//h1[@class='ArticleHead']/text()")
    time = doc.xpath("//p[@class='ArticlePublish' and position()=1]/span/text()")
    if not time:
        time = doc.xpath("//input[@class='article_created_on']/@value")

    if not title:
        title = doc.xpath("//meta[@name='title']/@content")

        if not title:
            title = doc.xpath("//title/text()")

    if title and time:
        title = str(title[0]).strip()
        time = str(time[-1]).strip()
        lines.insert(0,time)
        lines.insert(0,title)

    return lines


if text and any(line.strip() != "" for line in text):
    text = addnewstime(text, html_string)
    with open("tmp/texts/" + filename, "w", encoding="utf-8") as f:
#        f.write("\n".join([line.strip() if line.strip() != "" for line in text]))
        f.write("".join([line.strip() + "\n" if line.strip() != "" else "" for line in text])[:-1])

    print("Finished cleaning : ", filename)
else:
    print("Problem cleaning : ", filename)

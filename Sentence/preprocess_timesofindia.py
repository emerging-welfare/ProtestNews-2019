import sys
import re
import lxml.html
from fuzzywuzzy import fuzz

stoplist = ["RELATED", "From around the web", "More from The Times of India", "Recommended By Colombia",
            "more from times of india Cities","You might also", "You might also like", "more from times of india",
            "All Comments ()+^ Back to Top","more from times of india News","more from times of india TV",
            "more from times of india Sports","more from times of india Entertainment","more from times of india Life & Style",
            "more from times of india Business"]

stoplist2 = ["FOLLOW US","FOLLOW PHOTOS","FOLLOW LIFE & STYLE"]

filename = sys.argv[1]

with open("tmp/texts/" + filename, "r", encoding="utf-8") as f:
    text = f.read().splitlines()

with open("tmp/htmls/" + filename, "rb", encoding="utf-8") as g:
    html_string = g.read()


def deletesamesubstr(lines):
    i = 0
    while i <= len(lines)-1:
        isDeleted = False
        firstline = lines[i]
        firstline = re.sub(r"\W", r"", firstline)
        firstline = re.sub(r"<[^>]*>", r"", firstline)
        for j in range(i+1,len(lines)):
            secondline = lines[j]
            secondline = re.sub(r"\W", r"", secondline)
            if firstline.lower() in secondline.lower() and len(firstline)>22:
                del lines[i]
                isDeleted = True
                break

        if not isDeleted:
            i = i + 1

    return lines

def deletecertainstr(lines, stoplist, stoplist2):

    for i in range(0,len(lines)):
        firstline = lines[i]
        firstline = firstline.strip()
        if any(firstline == word for word in stoplist):
            for j in range(i, len(lines)):
                del lines[i]
            break

    n = 0
    while n < len(lines)-1:
        if not lines[n]:
            n = n + 1
            continue
        line = lines[n].strip()
        if any(line == word for word in stoplist2):
            del lines[n]
            continue
        n = n + 1

    return lines

def addnewstime(lines, html_string):

    doc = lxml.html.document_fromstring(html_string)
    title = doc.xpath("//h1[@class='heading1']/text()")
    time = doc.xpath("string(//span[@class='time_cptn'])")

    if not title:
        title = doc.xpath("//title/text()")

    if title and time:
        title = str(title[0]).strip()
        time = str(time).strip()
        if not any(fuzz.ratio(title,line)>70 for line in lines):
            lines.insert(0,time)
            lines.insert(0,title)

    return lines

    
text = deletesamesubstr(text)
if text:
    text = deletecertainstr(text, stoplist, stoplist2)
    if text and any(line.strip() != "" for line in text):
        text = addnewstime(text, html_string)
        text = deletesamesubstr(text)
        if text:
            with open("tmp/texts/" + filename, "w", encoding="utf-8") as f:
                f.write("\n".join([line.strip() if line.strip() != "" for line in text]))

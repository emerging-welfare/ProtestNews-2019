import sys
import re
import lxml.html
from fuzzywuzzy import fuzz

stoplist2 = ["ShareArticle","Updated:","MoreIn","SpecialCorrespondent","METRO PLUS","EDUCATION PLUS","PROPERTY PLUS","CINEMA PLUS","DISTRICT PLUS"]

stoplist3 = ["METRO PLUS","EDUCATION PLUS","PROPERTY PLUS","CINEMA PLUS","DISTRICT PLUS"]

filename = sys.argv[1]

with open("tmp/texts/" + filename, "r", encoding="utf-8") as f:
    text = f.read().splitlines()

with open("tmp/htmls/" + filename, "rb") as g:
    html_string = g.read()

def deletecertainstr(lines, stoplist):

    firsttime = True
    for i in range(0,len(lines)):
        firstline = lines[i]
        firstline = firstline.strip()
        if firsttime:
            if re.search(r"\d{2}:\d{2} IST", firstline):
                firsttime = False
            continue
        else:
            j = i
            n = len(lines)
            while j < n:
                line = lines[j].strip()
                time = re.search(r"\d{2}:\d{2}IST", line)
                if time or any(line == word for word in stoplist):
                    del lines[j]
                    n = n - 1
                    continue
                j = j + 1
            break

    return lines

def addnewstime(lines, html_string, stoplist):

    doc = str(html_string)
    place = re.search(r'var datelineStr\s*=\s*"([^"]*)"', doc)
    if place:
        place = place.group(1)

    doc = lxml.html.document_fromstring(html_string)
    title = doc.xpath("//h1[@class='artcl-nm-stky-text']/text()")
    if not place:
        place = doc.xpath("//meta[contains(@property,'section')]/@content")
        place = str(place[0])

    if not title:
        title = doc.xpath("//title/text()")

    if title:
        title = str(title[0]).strip()
        if not any(fuzz.ratio(title,line)>70 for line in lines):
            lines.insert(0,title)

    if place:
        place = place.strip()
        if place not in stoplist:
            lines.insert(0,place)

    return lines

    
if text:
    text = deletecertainstr(text, stoplist2)
    if text and any(line.strip() != "" for line in text):
        text = addnewstime(text, html_string, stoplist3)
        with open("tmp/texts/" + filename, "w", encoding="utf-8") as f:
#            f.write("\n".join([line.strip() if line.strip() != "" for line in text]))
            f.write("".join([line.strip() + "\n" if line.strip() != "" else "" for line in text])[:-2])

    print("Finished cleaning : ", filename)
else:
    print("Problem cleaning : ", filename)

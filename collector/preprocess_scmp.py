import sys
import re
import lxml.html

stoplist = ["Print Email","Video"]

stoplist2 = ["Viewed","Associated Press","Get updates direct to your inbox","Opinion"]

filename = sys.argv[1]

with open("tmp/texts/" + filename, "r", encoding="utf-8") as f:
    text = f.read().splitlines()

with open("tmp/htmls/" + filename, "r", encoding="utf-8") as g:
    html_string = g.read()

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
        line = lines[n]
        line = line.strip()
        if any(line == word for word in stoplist2):
            del lines[n]
            continue
        n = n + 1

    return lines

def addnewstime(lines, html_string):

    doc = lxml.html.document_fromstring(html_string)
    has_time = False
    for i,line in enumerate(lines):
        line = line.strip()
        if ("UPDATED : " in line):
            has_time = True
            del lines[i]
            break

    if not has_time:
        title = doc.xpath("//title/text()")
        time = doc.xpath('//div[@itemprop="dateCreated"]/text()')
        if title:
            title = title[0].strip()
            # Kept the typo, because we need to stick to the original preprocessing to get the same text, even if there was a mistake in the first place!
            if not any(re.sub(r"[ \n\r]\t]", r"", title) == re.sub(r"[ \n\r\t]", r"", line) for line in lines):
                lines.insert(0,title)

        if time:
            time = time[0].strip()
            lines.insert(0,time)

    return lines

    
if text:
    text = deletecertainstr(text, stoplist, stoplist2)
    if text and any(line.strip() != "" for line in text):
        text = addnewstime(text, html_string)
        with open("tmp/texts/" + filename, "w", encoding="utf-8") as f:
#            f.write("\n".join([line.strip() if line.strip() != "" for line in text]))
            f.write("".join([line.strip() + "\n" if line.strip() != "" else "" for line in text])[:-2])

    print("Finished cleaning : ", filename)
else:
    print("Problem cleaning : ", filename)

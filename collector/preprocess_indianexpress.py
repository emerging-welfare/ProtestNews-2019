import sys
import lxml.html

stoplist = ["Tags:","ALSO READ","Please read our before posting comments","TERMS OF USE: The views expressed in comments published on indianexpress.com are those of the comment writer's alone. They do not represent the views or opinions of The Indian Express Group or its staff. Comments are automatically posted live; however, indianexpress.com reserves the right to take it down at any time. We also reserve the right not to publish comments that are abusive, obscene, inflammatory, derogatory or defamatory."]

filename = sys.argv[1]

with open("tmp/texts/" + filename, "r", encoding="utf-8") as f:
    text = f.read().splitlines()

with open("tmp/htmls/" + filename, "rb") as g:
    html_string = g.read()

def deletecertainstr(lines, stoplist):

    for i in range(0,len(lines)):
        firstline = lines[i]
        firstline = firstline.strip()
        if any(firstline == word for word in stoplist):
            for j in range(i, len(lines)):
                del lines[i]
            break

    return lines

def addnewstime(lines, html_string):

    doc = lxml.html.document_fromstring(html_string)
    title = doc.xpath("//title/text()")
    time = doc.xpath("//div[@class='story-date']/text()")
    if time is None:
        time = doc.xpath("//div[@class='posted'/strong[last()]/text()")

    if time:
        lines.insert(0,"".join([i for i in time]))

    lines.insert(0,"".join([i for i in title]))

    return lines

    
if text:
    text = deletecertainstr(text, stoplist)
    if text and any(line.strip() != "" for line in text):
        text = addnewstime(text, html_string)
        with open("tmp/texts/" + filename, "w", encoding="utf-8") as f:
            #f.write("\n".join([line.strip() if line.strip() != "" for line in text]))
            f.write("".join([line.strip() + "\n" if line.strip() != "" else "" for line in text])[:-1])

    print("Finished cleaning : ", filename)
else:
    print("Problem cleaning : ", filename)

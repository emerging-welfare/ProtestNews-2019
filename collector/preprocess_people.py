#!/usr/bin/env python3
import sys
import lxml.html

filename = sys.argv[1]

with open("tmp/texts/" + filename, "r", encoding="utf-8") as f:
    text = f.read().splitlines()
    if not text:
        text = []

with open("tmp/htmls/" + filename, "rb") as f:
    html_string = f.read()

def add_title_time(lines, doc):
    title = doc.xpath("//div[@id='p_title']/text()")
    if not title:
        title = doc.xpath("//span[@id='p_title']/text()")
    if not title:
        title = doc.xpath("//div[@id='ivs_title']/text()")
    time = doc.xpath("//div[@id='ivs_publishtime']/text()")

    if not time:
        time = doc.xpath("//div[@id='p_publishtime']/text()")
    if not time:
        time = doc.xpath("//span[@id='p_publishtime']/text()")

    if time:
        time = "".join([i for i in time])
        if lines.count(time) == 0:
            lines.insert(1 if len(lines) > 1 else 0, time)
    else:
        print("Cannot get time for: ", filename)
    
    if title:
        title = "".join([i for i in title])
        if lines.count(title) == 0:
            lines.insert(0,title)
    else:
        print("Cannot get title for: ", filename)

    return lines

def is_allowed(x):
    if x is None or x == "":
        return False
    if x in ['Email | Print', '+', 'stumbleupon', 'More Pictures', 'Save Article', 'Click the "PLAY" button and listen. Do you like the online audio service here?','Good, I like it','Do you have anything to say?','Name']:
        return False
    if x.startswith('Source'):
        return False
    return True

text = list([x for x in [line.strip() for line in text] if is_allowed(x)])
if text and any(line.strip() != "" for line in text):
    doc = lxml.html.document_fromstring(html_string)
    text = add_title_time(text, doc)
    with open("tmp/texts/" + filename, "w", encoding="utf-8") as f:
        #f.write("\n".join([line.strip() if line.strip() != "" for line in text]))
        f.write("".join([line.strip() + "\n" if line.strip() != "" else "" for line in text])[:-1])

    print("Finished cleaning : ", filename)
else:
    print("Problem cleaning : ", filename)

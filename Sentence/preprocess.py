import pandas as pd
import sys
import re
import lxml.html
from fuzzywuzzy import fuzz

timesofindia_stoplist1 = ["RELATED", "From around the web", "More from The Times of India", "Recommended By Colombia",
            "more from times of india Cities","You might also", "You might also like", "more from times of india",
            "All Comments ()+^ Back to Top","more from times of india News","more from times of india TV",
            "more from times of india Sports","more from times of india Entertainment","more from times of india Life & Style",
            "more from times of india Business"]

timesofindia_stoplist2 = ["FOLLOW US","FOLLOW PHOTOS","FOLLOW LIFE & STYLE"]

indianexpress_stoplist1 = ["Tags:","ALSO READ","Please read our before posting comments","TERMS OF USE: The views expressed in comments published on indianexpress.com are those of the comment writer's alone. They do not represent the views or opinions of The Indian Express Group or its staff. Comments are automatically posted live; however, indianexpress.com reserves the right to take it down at any time. We also reserve the right not to publish comments that are abusive, obscene, inflammatory, derogatory or defamatory."]

thehindu_stoplist2 = ["ShareArticle","Updated:","MoreIn","SpecialCorrespondent","METRO PLUS","EDUCATION PLUS","PROPERTY PLUS","CINEMA PLUS","DISTRICT PLUS"]

scmp_stoplist1 = ["Print Email","Video"]

scmp_stoplist2 = ["Viewed","Associated Press","Get updates direct to your inbox","Opinion"]

filename = sys.argv[1]

df = pd.read_json(filename, orient="records", lines=True)
df["text"] = ""
df["html_string"] = ""
df["source"] = 0

for url in df.url.unique().tolist():
    els = df[df.url == url]
    text_file = re.sub(r":\/\/", r"___", url)
    text_file = re.sub(r"\/", r"_", text_file)
    with open("tmp/texts/" + text_file, "r", encoding="utf-8") as f:
        text = f.read().splitlines()
    with open("tmp/htmls/" + text_file, "rb", encoding="utf-8") as g:
        html_string = g.read()
    df.loc[df.url == url, "text"] = text
    df.loc[df.url == url, "html_string"] = html_string
    df.loc[df.url == url, "source"] = which_source(url)

df.loc[df.source == 1, "text"] = df[df.source == 1].text.apply(deletesamesubstr)
df = df[(df.text != "") & ("".join([line for line in df.text]) != "")]

df.loc[df.source.isin([1,3,4,5])] = df[df.sourceisin([1,3,4,5])].apply(deletecertainstr, axis=1)
df = df[(df.text != "") & ("".join([line for line in df.text]) != "")]

df = df.apply(addnewstime, axis=1)
df = df.drop(["html_string", "source"], axis=1)
df.text = df.text.apply(lambda x: "\n".join([line if line != "" for line in x]))

def which_source(url):
    if "timesofindia" in url:
        return 1
    elif "newindianexpress" in url:
        return 2
    elif "indianexpress" in url:
        return 3
    elif "thehindu" in url:
        return 4
    elif "scmp" in url:
        return 5
    else:
        print("No source : ", url)
        return 0

def choose_stoplists(source):
    if source == 1:
        return timesofindia_stoplist1, timesofindia_stoplist2
    elif source == 3:
        return indianexpress_stoplist1, []
    elif source == 4:
        return [], thehindu_stoplist2
    elif source == 5:
        return scmp_stoplist1, scmp_stoplist2
    else:
        print("Something wong : ", source)
    
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

def deletecertainstr(row):

    lines = row.text
    source = row.source
    stoplist1, stoplist2 = choose_stoplists(source)

    # Delete lines at the end of the doc
    if source in [1,3,5]:
        for i in range(0,len(lines)):
            firstline = lines[i]
            # firstline = firstline.strip()
            if any(firstline == word for word in stoplist1):
                for j in range(i, len(lines)):
                    del lines[i]
                break

    # Delete certain lines
    if source in [1,5]:
        n = 0
        while n < len(lines)-1:
            if not lines[n]:
                n = n + 1
                continue
            line = lines[n]
            # line = line.strip()
            if any(line == word for word in stoplist2):
                del lines[n]
                continue
            n = n + 1

    # Delete certain line or a repeating line containing a time value
    if source == 4:
        firsttime = True
        for i in range(0,len(lines)):
            firstline = lines[i]
            firstline = re.sub(r"\n|\r", r"", firstline)
            if firsttime:
                if re.search(r"\d{2}:\d{2} IST", firstline):
                    firsttime = False
                continue
            else:
                j = i
                n = len(lines)
                while j < n:
                    line = re.sub(r"\n|\r| ", r"", lines[j])
                    time = re.search(r"\d{2}:\d{2}IST", line)
                    if time or any(line == word for word in stoplist2):
                        del lines[j]
                        n = n - 1
                        continue
                    j = j + 1
                break

    row.text = lines

    return row

def addnewstime(row):

    html_string = row.html_string
    lines = row.text
    source = row.source

    if source == 4:
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
            place = re.sub(r"\n|\r", r"", place)
            if place in stoplist:
                lines.insert(0,place)

        row.text = lines
        return row
    
    doc = lxml.html.document_fromstring(html_string)
    if source == 1:
        title = doc.xpath("//h1[@class='heading1']/text()")
        time = doc.xpath("string(//span[@class='time_cptn'])")
        if not title:
            title = doc.xpath("//title/text()")
        if title:
            title = str(title[0]).strip()
        if title and time:
            time = str(time).strip()
            if not any(fuzz.ratio(title,line)>70 for line in lines):
                lines.insert(0,time)
                lines.insert(0,title)

    elif source == 2:
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

    elif source == 3:
        title = doc.xpath("//title/text()")
        time = doc.xpath("//div[@class='story-date']/text()")
        if time is None:
            time = doc.xpath("//div[@class='posted'/strong[last()]/text()")

        if time:
            lines.insert(0,time)

        lines.insert(0,title)

    elif source == 5:
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

        
    row.text = lines
    return row

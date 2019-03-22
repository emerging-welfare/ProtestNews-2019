import pandas as pd
import sys
import re
import logging

log_file = 'sentence_logging.log'
logging.basicConfig(level=logging.INFO,filename=log_file, filemode = "w",format='%(name)s - %(levelname)s - %(message)s')
print("Logging information stored in : %s"%log_file)

# We basically remove all the non-alphanumerical characters from our string and substring, then do the match. Later we map the resulting offsets to the original string we were searching.
def map_to_withW(i, j, text):
    tmp = re.findall(r"\W", text[i:j])
    while len(tmp) > 0:
        i = j
        j = j + len(tmp)
        tmp = re.findall(r"\W", text[i:j])

    return j

def get_som(match, text):
    i = 0
    som = match.start()
    som = map_to_withW(i, som, text)

    return som

def get_eom(match, text):

    som = get_som(match, text)
    i = som
    eom = som + match.end() - match.start()
    eom = map_to_withW(i, eom, text)

    return eom+1, som

# Calculates offset with the help of its neighbours. Then gets the corresponding text.
def fill_blank(row, els):
    # The end of span from the previous element is the start, and the start of span from the next element is the end.
    start = els[els.sent_num == row.sent_num - 1].iloc[0].offset.split(",")[1]
    end = els[els.sent_num == row.sent_num + 1].iloc[0].offset.split(",")[0]
    row.offset = start + "," + end
    row.sentence = row.text[int(start):int(end)]
    return row


filename = sys.argv[1]

df = pd.read_json(filename, orient="records", lines=True)
df["offset"] = ""
df["text"] = ""

nodoc_count = 0
nofirstmatch_count = 0
noanymatch_count = 0
total = 0
for url in df.url.unique().tolist():
    total +=1
    els = df[df.url == url]
    text_file = re.sub(r":\/\/", r"___", url)
    text_file = re.sub(r"\/", r"_", text_file)
    #print(text_file)
    try:
        with open("tmp/texts/" + text_file, "r", encoding="utf-8") as f:
            text = f.read()
    except:
        nodoc_count += 1
        df = df[df.url != url]
        logging.warning("Could not find news article with following url : %s"%url)
        continue

    df.loc[df.url == url, ["text"]] = text

    first_sent = els[els.sent_num == 1].sentence.iloc[0]
    if len(first_sent) >= 50:
        sep = int(len(first_sent) / 3)
    else:
        sep = int(len(first_sent) / 2)

    nonW_text = re.sub(r"\W", r"", text)
    start = re.search(re.sub(r"\W", r"", first_sent[len(first_sent) - sep:]), nonW_text)
    if start is None:
        nofirstmatch_count += 1
        df.loc[(df.url == url) & (df.sent_num == 1), ["offset"]] = "0,0" # Second sentence will contain the first sentence too.
    else:
        eom, som = get_eom(start, text)
        df.loc[(df.url == url) & (df.sent_num == 1), ["offset"]] = str(max(0, som-sep-1)) + "," + str(eom)

    sentences = els[(els.sent_num != 1) & (els.sentence != "REDACTED")]

    # The excluded urls are mainly coming from this try except. Need to solve this issue before release.
    try:
        for i in range(len(sentences)):
            sent = sentences.iloc[i]
            if len(sent.sentence) >= 50: # Arbitrary number. If the sentence is too small, use the whole sentence to match.
                sep = int(len(sent.sentence) / 5)
                match = re.search(re.sub(r"\W", r"", sent.sentence[:sep]), nonW_text)
                som = get_som(match, text)
                match = re.search(re.sub(r"\W", r"", sent.sentence[len(sent.sentence)-sep:]), nonW_text)
                eom, _ = get_eom(match, text)
            else:
                match = re.search(re.sub(r"\W", r"", sent.sentence), nonW_text)
                eom, som = get_eom(match, text)

            df.loc[(df.url == url) & (df.sent_num == sent.sent_num), ["offset"]] = str(som) + "," + str(min(eom, len(text)))
    except:
        logging.warning("Could not any match in following url : %s"%url)
        noanymatch_count += 1
        df = df[df.url != url]
        continue

# print("Total doc count : ", total)
# print("No doc count : ", nodoc_count)
# print("No first match count : ", nofirstmatch_count) # If the first sentence cannot be found in downloaded text
# print("No any match count : ", noanymatch_count) # If any odd numbered sentence other than first cannot be found in downloaded text
logging.info("Total doc count : %d" %total)
logging.info("No doc count : %d" %nodoc_count)
logging.info("No first match count %d: " %nofirstmatch_count) # If the first sentence cannot be found in downloaded text
logging.info("No any match count : %d" %noanymatch_count)

df = df[df.text.str.strip() != ""]

df.loc[df.sentence == "REDACTED"] = df[df.sentence == "REDACTED"].apply(lambda x: fill_blank(x, df[df.url == x.url]), axis=1)

df = df.drop(["text", "offset"], axis=1)
df.to_json(re.sub(r"\/(\w+)\/(\w+)\.json$", r"/output/\g<1>/\g<2>_filled.json", filename), orient="records", lines=True, force_ascii=False)

import pandas as pd
import sys
import re

filename = sys.argv[1]

df = pd.read_json(filename, orient="records", lines=True)
df["offset"] = ""
df["text"] = ""

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

def fill_blank(row, els):
    # The end of span from the previous element is the start, and the start of span from the next element is the end.
    start = els[els.sent_num == row.sent_num - 1].iloc[0].offset.split(",")[1]
    end = els[els.sent_num == row.sent_num + 1].iloc[0].offset.split(",")[0]
    row.offset = start + "," + end
    row.sentence = row.text[int(start):int(end)]
    return row

for url in df.url.unique().tolist():
    els = df[df.url == url]
    text_file = re.sub(r":\/\/", r"___", url)
    text_file = re.sub(r"\/", r"_", text_file)
    print(text_file)
    with open("tmp/texts/" + text_file, "r", encoding="utf-8") as f:
        text = f.read()

    df.loc[df.url == url, "text"] = text
    print(text)
    nonW_list = []
    for match in re.finditer(r"\W", text):
        nonW_list.append(match.start())

    first_sent = els[els.sent_num == 1].sentence.iloc[0]
    sep = int(len(first_sent) / 2)
    # print(first_sent)
    # print("--")
    # print(first_sent[sep:])
    
    #start = re.search(re.escape(first_sent[sep:]), text)
    nonW_text = re.sub(r"\W", r"", text)
    start = re.search(re.sub(r"\W", r"", first_sent[sep:]), nonW_text)

    eom, som = get_eom(start, text)

    # df.loc[(df.url == url) & (df.sent_num == 1), "offset"] = (max(0, som-sep-1), eom)
    df.loc[(df.url == url) & (df.sent_num == 1), "offset"] = str(max(0, som-sep-1)) + "," + str(eom)
    # print(text[som:eom+1])
    # print("--")
    # print(text[max(0, som-sep-1):eom+1])
    # print("-------------------------------")

    #end = re.search(re.escape(els[els["last"] == True].sentence.iloc[0]), text)
    # end = re.search(re.escape(els[els["last"] == True].sentence.iloc[0]), text)
    # print(start)
    # print(end.end())
    # df["text"] = text[start.start()-sep:end.end()-1]

    sentences = els[(els.sent_num != 1) & (els.sentence != "REDACTED")]
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

        # sentences.loc[sentences.sentence == sent.sentence, "offset"] = (som, min(eom, len(text)))
        sentences.loc[sentences.sentence == sent.sentence, "offset"] = str(som) + "," + str(min(eom, len(text)))

    df.loc[(df.url == url) & (df.sent_num != 1) & (df.sentence != "REDACTED")] = sentences

# df.to_csv("asd.csv", index=False)
df.loc[df.sentence == "REDACTED"] = df[df.sentence == "REDACTED"].apply(lambda x: fill_blank(x, df[df.url == x.url]), axis=1)
df = df.drop(["text", "offset"], axis=1)
df.to_csv(re.sub(r"\.json$", r".csv", filename), index=False)

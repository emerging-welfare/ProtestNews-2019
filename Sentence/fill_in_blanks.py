import pandas as pd
import sys
import re

filename = sys.argv[1]

df = pd.read_json(filename, orient="records", lines=True)

for url in df.url.unique().tolist():
    els = df[df.url == url]
    text_file = re.sub(r":\/\/", r"___", url)
    text_file = re.sub(r"\/", r"_", text_file)
    print(text_file)
    with open("tmp/texts/" + text_file, "r", encoding="utf-8") as f:
        text = f.read()

    print(re.escape(els[els.sent_num == 1].sentence.iloc[0]))
    print(re.escape(els[els["last"] == True].sentence.iloc[0]))
    start = re.search(re.escape(els[els.sent_num == 1].sentence.iloc[0]), text)
    end = re.search(re.escape(els[els["last"] == True].sentence.iloc[0]), text)
    print(start)
    print(end.span()[1])
    df["text"] = text[start:end+1]

# df.to_csv("asd.csv", index=False)

import pandas as pd
import sys
import re

filename = sys.argv[1]

df = pd.read_json(filename, orient="records", lines=True)
df["text"] = ""

for url in df.url.unique().tolist():

    text_file = re.sub(r":\/\/", r"___", url)
    text_file = re.sub(r"\/", r"_", text_file)
#    print(text_file)
    try:
        with open("tmp/texts/" + text_file, "r", encoding="utf-8") as f:
            text = f.read()
        df.loc[df.url == url, ["text"]] = text
    except:
#        print("Doc not found! : ", text_file)
        pass
#        df = df[df.url != url]

df.to_json(re.sub(r"\.json$", r"_filled.json", filename), orient="records", lines=True, force_ascii=False)

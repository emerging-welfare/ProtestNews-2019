import pandas as pd
import sys
import re
import logging

log_file = 'document_logging.log'
logging.basicConfig(level=logging.INFO,filename=log_file, filemode = "w",format='%(name)s - %(levelname)s - %(message)s')
print("Logging information stored in : %s"%log_file)

filename = sys.argv[1]

df = pd.read_json(filename, orient="records", lines=True)
df["text"] = ""
count = 0
total = 0
for url in df.url.unique().tolist():
    total +=1
    text_file = re.sub(r":\/\/", r"___", url)
    text_file = re.sub(r"\/", r"_", text_file)

    try:
        with open("tmp/texts/" + text_file, "r", encoding="utf-8") as f:
            text = f.read()
        df.loc[df.url == url, ["text"]] = text
    except:
        count +=1
        logging.warning("Could not download following url: %s" %url)

print("Could not download {} urls out of {}".format(count,total))
logging.info("Could not download {} urls out of {}".format(count,total))
df.to_json(re.sub(r"\.json$", r"_filled.json", filename), orient="records", lines=True, force_ascii=False)

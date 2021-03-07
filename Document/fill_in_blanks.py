import sys
import re
import logging
from os import path
import json

filename = sys.argv[1]
out_filename = re.sub(r"\/(\w+)\/(\w+)\.json$", r"/output/\g<1>/\g<2>_filled.json", filename)
out_file = open(out_filename, "w", encoding="utf-8")

log_file = re.sub(r"\/(\w+)\/(\w+)\.json$", r"/output/\g<1>/\g<2>.log", filename)
logging.basicConfig(level=logging.INFO,filename=log_file, filemode = "w",format='%(name)s - %(levelname)s - %(message)s')
print("Logging information stored in : %s"%log_file)

with open(filename, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

count = 0
total = 0
for line in lines:
    total +=1
    url = line["url"]
    filename = "tmp/text/" + url.replace("/", "_").replace(":", "_")
    if path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        line["text"] = text
        out_file.write(json.dumps(line) + "\n")

    else:
        count +=1
        logging.warning("Could not download following url: %s" %url)

logging.info("Could not download {} urls out of {}".format(count,total))

out_file.close()

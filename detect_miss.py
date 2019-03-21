import os
import pandas as pd
import re
import logging


root = ""
target_dir = "collector/tmp/texts"
json_path = "Sentence/trial.json"
json_filled_path = "Sentence/trial_filled.json"
output = "missing_news_urls.txt"

##update checking according to Osman's transformation
def check_url(url1,url_list):
    for url in url_list:
        if url1==url:## this will be changed with Osman's code
            return True
    return False

def map_name(filename):
    url = re.sub(r"___", r"://", filename)
    url = re.sub(r"_", r"/", url)
    return url

def detect_miss(target_dir,jsonfile,filledjsonfile,log_file):
    misses = []
    count = 0
    df = pd.read_json(jsonfile,orient = "records", lines = True)
    df_filled = pd.read_json(filledjsonfile,orient = "records", lines = True)
    or_sample_size = len(df.get("id"))
    fi_sample_size = len(df_filled.get("id"))
    samp_c = 0
    all_urls = set()
    filled_urls = set()
    filled_misses = set()
    for r2 in df_filled.iterrows():
        filled_urls.add(r2[1]["url"])
    all_files = list(map(lambda x: map_name(x),os.listdir(target_dir)))
    for row in df.iterrows():
        url = row[1]["url"]
        if not check_url(url,all_files):
            if url not in misses:
                misses.append(url)
                count+=1
                logging.warning("Could not downloaded the following news article: %s"%url)
            #samp_c +=1
        if url not in filled_urls:
            if url not in filled_misses:
                filled_misses.add(url)
                logging.warning("Missing in filled json: %s"%url)
            logging.warning("Missing sample with id : %s"%row[1]["id"])
        all_urls.add(url)
    print("Missing {} out of {} news in filled json ".format(len(filled_misses) , len(all_urls)))
    print("Missing {} out of {} samples in total ".format(fi_sample_size , or_sample_size))
    print("Could not download {} news in total out of {} news".format(count,len(all_urls)))
    print("Writing missing news' urls into: %s"%log_file)
    outf = open(log_file,"w")
    for miss in misses:
        outf.write(miss)
        outf.write("\n")
    outf.close()
if __name__ == "__main__":
    logging.basicConfig(filename='sentence_level_logging.log', filemode = "w",format='%(name)s - %(levelname)s - %(message)s')
    detect_miss(os.path.join(root,target_dir),os.path.join(root,json_path), os.path.join(root,json_filled_path),output)

import os
import pandas as pd
root = "ProtestNews-2019/"
target_dir = "collector/tmp/texts"
json_path = "Sentence/trial.json"
output = "sentence_log"

##update checking according to Osman's transformation
def check_url(url1,url_list):
    for url in url_list:
        if url1==url:## this will be changed with Osman's code
            return True
    return False


def detect_miss(target_dir,jsonfile,log_file):
    misses = []
    count = 0
    df = pd.read_json(jsonfile,orient = "records", lines = True)
    urls = set(df.get("url"))
    all_files = os.listdir(target_dir)
    print(all_files[:10])
    for url in urls:
        if not check_url(url,all_files):
            if url not in misses:
                misses.append(url)
                count+=1
    print("Could not download {} news in total out of {} news".format(count,len(urls)))
    print("Writing missing news' urls into: %s"%log_file)
    outf = open(log_file,"w")
    for miss in misses:
        outf.write(miss)
        outf.write("\n")
    outf.close()
if __name__ == "__main__":
    detect_miss(os.path.join(root,target_dir),os.path.join(root,json_path),output)

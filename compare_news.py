import pandas as pd
import os
#root = "ProtestNews-2019/"
orig_json_path = "trial_small.json"
filled_json_path = "trial_small_filled.json"
output = "document_level_log"
def edit_distance(seq1,seq2):
    edits = [[0 for i in range(len(seq2)+1)]for j in range(len(seq1)+1)]
    for i in range(0,len(seq1)):
        for j in range(0,len(seq2)):
            if seq1[i]==seq2[j]:
                edits[i+1][j+1] = min(edits[i][j+1]+1,edits[i][j],edits[i+1][j]+1)
            else:
                edits[i+1][j+1] = min(edits[i][j+1],edits[i][j],edits[i+1][j])+1
    return edits[-1][-1]


def check_url(url1,url_list):
    for url in url_list:
        if url1==url:## this will be changed with Osman's code
            return True
    return False


## look at the edit distance between news articles and cleaned version
## report missing news articles and also
def compare_cleaned(initial_json,filled_json,log_file,threshold = 0.1):
    fill_json = pd.read_json(filled_json,orient= "records",lines=True)
    init_json = pd.read_json(initial_json,orient= "records",lines=True)
    miss_count = 0
    dirty_count = 0
    dirty_urls =[]
    orgs = fill_json.get("org_text")
    texts = fill_json.get("text")
    urls = init_json.get("url")
    filled_urls = fill_json.get("url")
    for url in urls:
        if not check_url(url,filled_urls):
            miss_count +=1
            #print(url)
    print("Missing {} news articles out of {} total ".format(miss_count,len(filled_urls)))
    for text,org,url in zip(texts,orgs,filled_urls):
        N = (len(text)+len(org))/2.0 ## normalization denominator for edit distance
        dist = edit_distance(text,org)
        if dist/N > threshold:
            dirty_count += 1
            dirty_urls.append(url)
            print(url)
    print("Number of Dirty downloads: {} out of {} news articles".format(dirty_count,len(filled_urls)))
    outf = open(log_file,"w")
    print("Writing dirty downloaded news into %s"%log_file)
    for dirty in dirty_urls:
        outf.write(dirty+"\n")
    outf.close()
if __name__ == "__main__":
    compare_cleaned(orig_json_path,filled_json_path,output)

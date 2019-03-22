import glob
import pandas as pd
import os
root = "ProtestNews-2019/Sentence"
jsons = list(filter(lambda x : "filled" not in x,glob.glob(os.path.join(root,"*.json"))))
#filledjsons = list(filter(lambda x : "filled" in x,glob.glob("ProtestNews-2019/Sentence/*.json")))
misses = {}
tot = 0
for j in jsons:
    name = j[len(root)+1:]
    misses[name] = set()
    dj = pd.read_json(j,orient= "records",lines=True)
    df = pd.read_json(j[:-5]+"_filled"+".json",orient= "records",lines=True)
    df_ids = []
    for i in df.iterrows():
        df_ids.append(i[1]["id"])
        #print(i[1]["id"])
    for item in dj.iterrows():
        if  item[1]["id"] not in df_ids:
            misses[name].add(item[1]["url"])
    out = open(name+"_missing_urls","w")
    for miss in misses[name]:
        out.write(miss+"\n")
    print("Number of missing urls in {} : {}".format(name,len(misses[name])))
    out.close()

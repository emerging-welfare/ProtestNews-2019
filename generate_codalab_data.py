import os
import glob
import pandas as pd
import sys
root_folder = "/Users/ardaakdemir/Desktop/koc/bitbucket_repo/corpus/Document/ProtestNews2019"

## this script generates the data to be uploaded to codalab in " id label "" format
## the script generates data for all the json files inside the root folder
## the first argument given denotes the root folder path
def generatecodalabdata(root_folder):
    json_file_names = glob.glob(os.path.join(root_folder,"*.json"))
    ## i love using map and lambda
    sol_file_names = list(map(lambda x : x[len(root_folder)+1:-4]+"solution",json_file_names))
    data_file_names = list(map(lambda x : x[len(root_folder)+1:-4]+"data",json_file_names))
    for o2f,of,jf in zip(data_file_names,sol_file_names,json_file_names):
        df = pd.read_json(jf,orient= "records",lines=True)
        d_out  = open(of,"w")
        dd_out = open(o2f,"w")
        for row in df.iterrows():
            row_id = str(row[1]["id"])
            label =  str(row[1]["label"])
            d_out.write(row_id+"\t"+label+"\n")
            dd_out.write(row_id+"\n")
        d_out.close()
        dd_out.close()

if __name__ == "__main__":
    path_to_jsons = root_folder
    if len(sys.argv)>1:
        path_to_jsons = sys.argv[1]
    generatecodalabdata(path_to_jsons)

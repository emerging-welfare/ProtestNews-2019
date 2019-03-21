Sadly we cannot share the whole text of the articles we labelled/annotated due to the copyright infringment laws. \
Therefore we prepared three scripts for Document, Sentence and Token level data to automatically download from provided urls and "fill in the blanks". \
There is no way to make this whole process lossless due to the fact that those tricky, everchanging htmls. \
Even though we try to compensate for every possible problem, there will be some changes from the original data we labelled. So we evaluate how this small change effects a baseline model, and share the results. \
\
To get your data ready, you need to go into each of the folders (Document, Sentence and Token) and run `bash run.sh`
### Requirements
Firstly install additional requirements in requirements_additional. You can do so by running `apt-get install` line in Ubuntu. For python packages, you need to visit the github pages and follow install instructions. \
For python2 requirements, run -> `pip2 install -r requirements2.txt` \
For python3 requirements, run -> `pip3 install -r requirements3.txt`

### Logs
You can find the log file for scrapy and selenium as ProtestNews-2019/collector/log.txt and ProtestNews-2019/collector/ghostdriver.log respectively.\
For the log file of run.sh, you can check your current folder (Sentence or Document).
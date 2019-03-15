import sys
from goose import Goose
import codecs

filename=sys.argv[1]

try:
    with open("tmp/htmls/" + filename, "rb") as f:
        html = f.read()
except:
    print("No file named as : ", filename)
    sys.exit(0)
    
g = Goose()
article = g.extract(raw_html=html)

with codecs.open("tmp/texts/" + filename, "w", "utf-8") as g:
    g.write(article.cleaned_text)

print("Finished html-to-text : " + filename)

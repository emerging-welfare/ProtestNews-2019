from boilerpipe.extract import Extractor
import sys
import codecs

filename = sys.argv[1]

try:
    if "scmp" in filename:
#        with open("tmp/htmls/" + filename, "r", encoding="utf-8") as f:
        with open("tmp/htmls/" + filename, "r") as f:
            data = f.read()
    else:
        with open("tmp/htmls/" + filename, "rb") as f:
            data = f.read()
except:
    print("No file named as : " + filename)
    sys.exit(0)

extractor = Extractor(extractor='ArticleExtractor', html=data)

extracted_text = extractor.getText()

with codecs.open("tmp/texts/" + filename, "w", "utf-8") as g:
    g.write(extracted_text)

print("Finished html-to-text : " + filename)

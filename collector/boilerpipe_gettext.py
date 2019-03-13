from boilerpipe.extract import Extractor
import sys
import codecs

filename = sys.argv[1]

try:
    with open("tmp/htmls/" + filename, "rb") as f:
        data = f.read()
except:
    print("No file named as : ", filename)
    sys.exit(0)

extractor = Extractor(extractor='ArticleExtractor', html=data)

extracted_text = extractor.getText()

with codecs.open("tmp/texts/" + filename, "w", "utf-8") as g:
    g.write(extracted_text)

print("Finished : " + filename)

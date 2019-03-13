import justext
import sys

filename=sys.argv[1]

try:
    with open("tmp/htmls/" + filename, "r") as f:
        html = f.read()
except:
    print("No file named as : ", filename)
    sys.exit(0)

ofile = open("tmp/texts/" + filename, "a", encoding="utf-8")

paragraphs = justext.justext(html,justext.get_stoplist("English"))
for paragraph in paragraphs:
    if not paragraph.is_boilerplate:
        ofile.write(paragraph.text + "\n")

ofile.close()

print("Finished : ", filename)

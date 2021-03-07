import re

def stringify_children(node):
    s = node.text
    if s is None:
        s = ''
    if node.tail:
        s = s + node.tail
    for child in node:
        if child.tag != "div":
            s += '\n' + re.sub(r" {2,}|\n|\r|\t", r"", stringify_children(child))
    return s

def remove_all_lines_after_stoplist(text, stoplist):
    lines = text.splitlines()
    for i in range(0,len(lines)):
        firstline = lines[i]
        firstline = re.sub(r"\n|\r", r"", firstline)
        if any(firstline == word for word in stoplist):
            for j in range(i, len(lines)):
                del lines[i]
            break

    text = "\n".join([line for line in lines if re.search("\S", line)])
    return text

def remove_stoplist_lines(text, stoplist):
    lines = text.splitlines()
    text = "\n".join([line for line in lines if re.search("\S", line) and (line.strip() not in stoplist)])
    return text

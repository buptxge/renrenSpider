import re

text = "good morning"
m = re.match(r"goo",text)
print m.group(0)

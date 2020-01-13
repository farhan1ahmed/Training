import xml.etree.ElementTree as ET
lines = int(input("Enter number of lines: "))
xml = ''
print("Enter XML text:")
for line in range(lines):
    xml += input()
tree = ET.ElementTree(ET.fromstring(xml))
score = 0
for elem in tree.iter():
    score += len(elem.attrib)
print(score)

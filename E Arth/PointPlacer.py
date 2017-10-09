import os

filepath = "D:\\Users\\Charles Turvey\\Documents\\Python\\Projects\\E Arth\\Points"
i = 1
while os.path.exists(filepath + str(i) + ".kml"):
    i += 1
filepath = filepath + str(i) + ".kml"
file = os.open(filepath, os.O_APPEND | os.O_CREAT | os. O_RDWR)
writestring = lambda words: os.write(file, bytes(words, "UTF-8"))

def addplacemark(name, description, points):
    writestring("  <Document>"
                "    <Placemark>\n"
                "      <name>%s</name>\n"
                "      <description>%s</description>\n"
                "      <LineString>\n"
                "        <coordinates>\n" %(name, description))
    for i in range(len(points)):
        point = points[i]
        writestring("        %s,%s\n" %(point[0], point[1]))
    writestring("        </coordinates>\n"
                "      </LineString>\n"
                "    </Placemark>\n"
                "  </Document>\n")

def makeline(start, finish):


top = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
      "<kml>\n"
bottom = "</kml>"

writestring(top)
pattern = []
for i in range(30, 390):
    pattern.append(((i % 360) - 180, 60))
pattern += [(150,60),
            (-30,60),
            (-60,60),
            (60,60),
            (-150,60),
            (-30,60),
            (120,60),
            (-120,60),
            (30,60)]
addplacemark("Bleh", "Some places with things", pattern)
writestring(bottom)

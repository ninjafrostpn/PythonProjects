import os

blankdocument = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>{5}.kml</name>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>{1}</color>
			<width>{2}</width>
		</LineStyle>
	</Style>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>{1}</color>
			<width>{2}</width>
		</LineStyle>
	</Style>
	<Placemark>
		<name>{0}</name>
		<description>{3}</description>
		<styleUrl>#m_ylw-pushpin</styleUrl>
		<LineString>
			<tessellate>1</tessellate>
			<altitudeMode>absolute</altitudeMode>
			<coordinates>
				{4}
			</coordinates>
		</LineString>
	</Placemark>
</Document>
</kml>
"""

def fromGPX(rawGPX):
    start = rawGPX.index("<name>") + 6
    end = rawGPX.index("</name>", start)
    name = rawGPX[start:end]
    pts = []
    end = 0
    while True:
        try:
            pt = []
            start = rawGPX.index("<trkpt lat=\"", end) + 12
            end = rawGPX.index("\" lon=", start)
            pt.append(float(rawGPX[start:end]))
            start = end + 7
            end = rawGPX.index("\">", start)
            pt.insert(0, float(rawGPX[start:end]))
            start = end + 13
            end = rawGPX.index("</ele>", start)
            pt.append(float(rawGPX[start:end]))
            pts.append(pt)
        except ValueError as e:
            break
    return pts, name

def toKML(pts, name="", filename=None, col=(255, 165, 0), width=1, desc=""):
    if filename is None:
        filename = name
    if filename.endswith(".gpx"):
        filename = filename[:-4]
    hexcol = "ff" + hex((((col[0] << 8) + col[1]) << 8) + col[1])[2:]
    ptstring = " ".join([",".join([str(float(i)) for i in pt]) for pt in pts])
    return blankdocument.format(name, hexcol, width, desc, ptstring, filename)

def readfile(filepath):
    file = os.open(filepath, os.O_APPEND | os.O_RDWR)
    raw = ""
    while True:
        part = str(os.read(file, 100))[2:-1]
        if part == "":
            break
        else:
            raw += part
    return raw

def convertfile(filepath):
    GPXdata = readfile(filepath)
    KMLdata = toKML(*fromGPX(GPXdata))
    with open(filepath[:-4] + ".kml", 'w', newline='') as KMLfile:
        KMLfile.write(KMLdata)


convertfile(r"D:\Users\Charles Turvey\Documents\Wight\1 - To the estuary.gpx")
convertfile(r"D:\Users\Charles Turvey\Documents\Wight\2 - Up from the estuary.gpx")
convertfile(r"D:\Users\Charles Turvey\Documents\Wight\3 - To baking.gpx")
convertfile(r"D:\Users\Charles Turvey\Documents\Wight\4 - To the ferry.gpx")
convertfile(r"D:\Users\Charles Turvey\Documents\Wight\5 - To the beach.gpx")
convertfile(r"D:\Users\Charles Turvey\Documents\Wight\6 - Back to the ferry.gpx")
convertfile(r"D:\Users\Charles Turvey\Documents\Wight\7 - Night Ride.gpx")

#print(toKML([(0, i, 1000) for i in range(0, 60, 10)], name="TESTPATH2", desc="Yes"))

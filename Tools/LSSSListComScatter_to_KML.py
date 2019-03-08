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


def fromLCS(rawLCS):
    lats = []
    lons = []
    pts = []
    Npos = 0
    Epos = 0
    while Npos < len(rawLCS) and Epos < len(rawLCS):
        try:
            Npos = rawLCS.index("  N", Epos) + 2
            if rawLCS[Npos + 1] == 'A':
                Npos = rawLCS.index("  N", Npos + 5) + 2
            Epos = rawLCS.index(" E", Npos) + 1
            lats.append(str(int(rawLCS[Npos + 1: Npos + 3]) + (float(rawLCS[Npos + 4: Npos + 8]) / 60)))
            lons.append(str(int(rawLCS[Epos + 1: Epos + 4]) + (float(rawLCS[Epos + 5: Epos + 9]) / 60)))
            pts.append((lons[-1], lats[-1]))
            print((lons[-1], lats[-1]))
        except:
            break
    return pts


def toKML(pts, name="", filename=None, col=(255, 165, 0), width=1, desc=""):
    if filename is None:
        filename = name
    if filename.endswith(".txt"):
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
    trackdata = readfile(filepath)
    KMLdata = toKML(fromLCS(trackdata))
    with open(filepath[:-3] + "kml", 'w', newline='') as KMLfile:
        KMLfile.write(KMLdata)


convertfile(r"E:\TRAINING - BIOMASS ESTIMATION\Sørfjorden data\ListComScatter_F038000_T2_L6113.1-6216.9.txt")

#print(toKML([(0, i, 1000) for i in range(0, 60, 10)], name="TESTPATH2", desc="Yes"))

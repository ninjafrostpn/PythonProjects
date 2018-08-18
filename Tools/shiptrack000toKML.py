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

def from000(raw000):
    lats = []
    lons = []
    pts = []
    Npos = 0
    Wpos = 0
    while Npos < len(raw000) and Wpos < len(raw000):
        try:
            Npos = raw000.index(",N,", Wpos)
            Wpos = raw000.index(",W,", Npos)
            lats.append("{}.{}".format(str(float(raw000[Npos - 11: Npos - 9])),
                                       str(float(raw000[Npos - 9: Npos])/60)))
            lons.append("-{}.{}".format(str(float(raw000[Npos - 12: Npos - 9])),
                                        str(float(raw000[Npos - 9: Npos])/60)))
            print(lats, lons)
            pts.append((lats[-1], lons[-1]))
        except:
            break
    return pts

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
    trackdata = readfile(filepath)
    KMLdata = toKML(from000(trackdata))
    with open(filepath[:-4] + ".kml", 'w', newline='') as KMLfile:
        KMLfile.write(KMLdata)


convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_000n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_001n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_002n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_003n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_004n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_005n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_006n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_007n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_008n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_009n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_010n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_011n.000")
convertfile(r"D:\Users\Charles Turvey\Documents\Course Materials\Year 2\Semester 2\SOES2027 Coastal and Estuarine 2\Plymouth\USB\Offshore Data\ADCP 03-07-18\Plym_2018_012n.000")

#print(toKML([(0, i, 1000) for i in range(0, 60, 10)], name="TESTPATH2", desc="Yes"))

import os

blankdocument = ('<?xml version="1.0" encoding="UTF-8"?>'
                 '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
                 '<Document>\n'
                 '    <name>{5}.kml</name>\n'
                 '    <StyleMap id="m_ylw-pushpin">\n'
                 '        <Pair>\n'
                 '            <key>normal</key>\n'
                 '            <styleUrl>#s_ylw-pushpin</styleUrl>\n'
                 '        </Pair>\n'
                 '        <Pair>\n'
                 '            <key>highlight</key>\n'
                 '            <styleUrl>#s_ylw-pushpin_hl</styleUrl>\n'
                 '        </Pair>\n'
                 '    </StyleMap>\n'
                 '    <Style id="s_ylw-pushpin">\n'
                 '        <IconStyle>\n'
                 '            <scale>1.1</scale>\n'
                 '            <Icon>\n'
                 '                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
                 '            </Icon>\n'
                 '            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
                 '        </IconStyle>\n'
                 '        <LineStyle>\n'
                 '            <color>{1}</color>\n'
                 '            <width>{2}</width>\n'
                 '        </LineStyle>\n'
                 '    </Style>\n'
                 '    <Style id="s_ylw-pushpin_hl">\n'
                 '        <IconStyle>\n'
                 '            <scale>1.3</scale>\n'
                 '            <Icon>\n'
                 '                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
                 '            </Icon>\n'
                 '            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
                 '        </IconStyle>\n'
                 '        <LineStyle>\n'
                 '            <color>{1}</color>\n'
                 '            <width>{2}</width>\n'
                 '        </LineStyle>\n'
                 '    </Style>\n'
                 '    <Placemark>\n'
                 '        <name>{0}</name>\n'
                 '        <description>{3}</description>\n'
                 '        <styleUrl>#m_ylw-pushpin</styleUrl>\n'
                 '        <LineString>\n'
                 '            <tessellate>1</tessellate>\n'
                 '            <altitudeMode>absolute</altitudeMode>\n'
                 '            <coordinates>\n'
                 '                {4}\n'
                 '            </coordinates>\n'
                 '        </LineString>\n'
                 '    </Placemark>\n'
                 '{6}'
                 '</Document>\n'
                 '</kml>')

blankpin = ('  <Placemark>\n'
            '    <name>{1}</name>'
            '    <description>{2}</description>\n'
            '    <styleUrl>#pointstyle</styleUrl>\n'
            '    <Point>\n'
            '      <coordinates>{0},0</coordinates>\\nn'
            '    </Point>\n'
            '  </Placemark>\n')


def fromLCS(rawLCS):
    pts = []
    Npos = 0
    Epos = 0
    while Npos < len(rawLCS) and Epos < len(rawLCS):
        try:
            Npos = rawLCS.index("  N", Epos) + 2
            if rawLCS[Npos + 1] == 'A':
                Npos = rawLCS.index("  N", Npos + 5) + 2
            Epos = rawLCS.index(" E", Npos) + 1
            pts.append((str(int(rawLCS[Epos + 1: Epos + 4]) + (float(rawLCS[Epos + 5: Epos + 9]) / 60)),
                        str(int(rawLCS[Npos + 1: Npos + 3]) + (float(rawLCS[Npos + 4: Npos + 8]) / 60)),
                        rawLCS[Npos: Epos + 9]))
        except:
            break
    return pts


def toKML(pts, name="", filename=None, col=(255, 165, 0), width=1, desc=""):
    if filename is None:
        filename = name
    if filename.endswith(".txt"):
        filename = filename[:-4]
    filename.replace(".", "-")
    hexcol = "ff" + hex((((col[0] << 8) + col[1]) << 8) + col[1])[2:]
    ptstring = " ".join([",".join([str(float(i)) for i in pt[:2]]) for pt in pts])
    pinstring = "".join([blankpin.format(",".join([str(c) for c in pt[:2]]), i, pt[2]) for i, pt in enumerate(pts)])
    return blankdocument.format(name, hexcol, width, desc, ptstring, filename, pinstring)


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

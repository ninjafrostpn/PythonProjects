import os, csv

def extracttag(data, tag):
    start = data.index("<{}>".format(tag)) + len(tag) + 2
    end = data.index("</{}".format(tag))
    return data[start: end], end + len(tag) + 3

def parse(data):
    data = extracttag(data, "DiveSamples")[0]
    samples = [("Time", "Depth", "Temperature", "AveragedTemperature")]
    while len(data) > 0:
        sampledata, nextindex = extracttag(data, "Dive.Sample")
        sample = (extracttag(sampledata, "Time")[0],
                  extracttag(sampledata, "Depth")[0],
                  extracttag(sampledata, "Temperature")[0],
                  extracttag(sampledata, "AveragedTemperature")[0])
        samples.append(sample)
        data = data[nextindex:]
    return samples

def convertfile(filepath):
    file = os.open(filepath, os.O_APPEND | os.O_RDWR)
    raw = ""
    while True:
        part = str(os.read(file, 100))[2:-1]
        if part == "":
            break
        else:
            raw += part
    sheet = parse(raw)
    with open(filepath[:-4] + ".csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in sheet:
            csvwriter.writerow(row)
    print("\n".join(["".join(["{:20} ".format(j) for j in i]) for i in parse(raw)]) + "\n")

def main(*args):
    print(args)
    if len(args) == 0:
        print("No dive xml given")
    else:
        for path in args[0]:
            if path[-4:] == ".xml":
                print("Converting ", path)
                convertfile(path)
            else:
                for filepath in os.listdir(path):
                    if filepath[-4:] == ".xml":
                        print("Converting ", filepath)
                        convertfile(path + "\\" + filepath)

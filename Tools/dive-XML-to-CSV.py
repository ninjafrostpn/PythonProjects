import os, sys, csv

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

def main(*args):
    if len(args) == 0:
        print("No dive xml given")
    else:
        for filepath in args[0]:
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
                for line in sheet:
                    csvwriter.writerow(line)
            print("\n".join(["".join(["{:20} ".format(j) for j in i]) for i in parse(raw)]))

if __name__ == "__main__":
    main(sys.argv[1:])

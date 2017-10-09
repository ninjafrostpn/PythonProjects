import os, pygame, math
from pygame.locals import *

dirname = input("Input directory\n>>> ")
pygame.init()
screen = pygame.display.set_mode((700, 700))
w = screen.get_width()
h = screen.get_height()
precision = 0.01

filenames = os.listdir(dirname)
print(filenames)

filesizes = []
failedfiles = []
for filename in filenames:
    try:
        filesizes.append(os.stat(dirname + "\\" + filename).st_size)
    except PermissionError:
        failedfiles.append(filenames.pop(filenames.index(filename)))
print(filesizes)
print(failedfiles)

filesizetotal = sum(filesizes)
print(filesizetotal)

filesizepercentages = [filesize / filesizetotal for filesize in filesizes]
print(filesizepercentages)
print(sum(filesizepercentages))

filesizecumulativepercentages = [sum(filesizepercentages[:i]) for i in range(len(filesizepercentages))]
print(filesizecumulativepercentages)

angles = [360 * percentage for percentage in filesizecumulativepercentages]
print(angles)

sectorcols = []
for i in range(len(filenames)):
    colpercent = (i + 1) / len(filenames)
    sectorcols.append((int(255 * colpercent), int(255 * colpercent * 3) % 256, int(255 * colpercent * 7) % 256))
    
filedata = "Successful Checks\n---------------\n"
for i in range(len(filenames)):
    filedata += filenames[i] + ":\n" + str(filesizes[i]) + " bytes\n"
filedata += "\nFailed Checks\n---------------\n"
for i in range(len(failedfiles)):
    filedata += failedfiles[i] + "\n"
print(filedata)

while True:
    screen.fill(0)
    
    i = 0
    j = (i + 1) % len(filenames)
    counter = 0
    pt2 = (350, 100)
    while counter < angles[-1]:
        sectorcol = sectorcols[i]
        while counter < angles[j]:
            pt1 = pt2
            pt2 = ((w/2) + (250 * math.cos(math.radians(counter))), (h/2) + (250 * math.sin(math.radians(counter))))
            pygame.draw.polygon(screen, sectorcol, ((w/2,h/2), pt1, pt2), 0)
            counter += precision
        i += 1
        j = (i + 1) % len(filenames)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()

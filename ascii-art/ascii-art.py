import cv2
import numpy as np

charsourceimg = cv2.cvtColor(cv2.imread(r"D:\Users\Charles Turvey\Documents\Python\Projects\ascii-art\letnum.png"), cv2.COLOR_RGB2GRAY)
# _, charsourceimg = cv2.threshold(charsourceimg, 128, 255, cv2.THRESH_BINARY)

charcolumns = np.int32([np.sum(charsourceimg[:, i] < 150) > 0 for i in range(charsourceimg.shape[1])])
charcolumnsstr = str(bytes(np.array([0, 1], dtype="string_")[charcolumns]))[2:-1]
# print(charcolumnsstr)

charnames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
charimgs = []
start = 0
end = 0
for charname in charnames:
    charstart = charcolumnsstr.index("1", end)
    end = charcolumnsstr.index("0", charstart)
    charimgs.append(charsourceimg[:, start:end])
    start = end

inputimg = cv2.cvtColor(cv2.imread(r"D:\Users\Charles Turvey\Pictures\Art\Wah\WahFace.png"), cv2.COLOR_RGB2GRAY)
# _, inputimg = cv2.threshold(inputimg, np.mean(inputimg) + 20, 255, cv2.THRESH_BINARY)

currx = 0
curry = 0
line = ""
while curry <= inputimg.shape[0]:
    scores = []
    for charimg in charimgs:
        inrgt = min(inputimg.shape[1], currx + charimg.shape[1])
        inbtm = min(inputimg.shape[0], curry + charimg.shape[0])
        charrgt = inrgt - currx
        charbtm = inbtm - curry
        scores.append(np.sum(np.abs(charimg[:charbtm, :charrgt] - inputimg[curry: inbtm, currx: inrgt])) / (255 * np.prod(charimg.shape)))
    besti = np.argmin(scores)
    bestimg = charimgs[besti]
    # cv2.imshow("char", bestimg)
    bestchar = charnames[besti]
    # print(currx, curry, "->", np.argmin(scores), "({})".format(bestchar))
    inrgt = min(inputimg.shape[1], currx + bestimg.shape[1])
    inbtm = min(inputimg.shape[0], curry + bestimg.shape[0])
    charrgt = inrgt - currx
    charbtm = inbtm - curry
    inputimg[curry: inbtm, currx: inrgt] = bestimg[:charbtm, :charrgt]
    line += bestchar
    currx += bestimg.shape[1]
    if currx >= inputimg.shape[1]:
        curry += bestimg.shape[0]
        currx = 0
        print(line)
        line = ""
    cv2.imshow("output", inputimg)
    cv2.waitKey(1)
cv2.waitKey()

import cv2

lines = ["a so",
         "salty",
         "is a veryvery",
         "so salt",
         "so very",
         "salt",
         "is a so",
         "salty"]

positions = [(9, 65),
             (9, 85),
             (248, 31),
             (374, 184),
             (226, 268),
             (226, 288),
             (428, 354),
             (428, 374)]

img = cv2.imread(r"So Salty (no words).png")

for i, line in enumerate(lines):
    response = input("%s >>> " % line)
    cv2.putText(img, line if response == "" else response, positions[i][:2], 5, 1, (255, 255, 255))

cv2.imshow("", img)
cv2.waitKey()

import numpy as np
import cv2
import pygame
from pygame.locals import *
from time import time

path = "Slo-Time Videos"

# Open Webcam
cap = cv2.VideoCapture(0)  # 1 signifies the second available camera device
fourcc = cv2.VideoWriter_fourcc(*"XVID")  # The protocol used for video

# Define some colours
white = (255, 255, 255)
black = 0
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 0, 255)


# Function for outputting seconds as hoursminutesseconds
def HMS(val):
    s = val % 60
    m = (val - s) % 3600
    h = (val - (m + s))
    return "{:n}h{:n}m{:.2f}s".format(h / 3600, m / 60, s)


# Set up the pygame window
pygame.init()
pygame.display.set_caption("Slo-Time")
screen = pygame.display.set_mode((1000, 480))
w = screen.get_width()
h = screen.get_height()

# Load up a nice font
smallfont = pygame.font.Font(r"D:\Users\Charles Turvey\Documents\Python\Projects\OpenSans-Regular.ttf", 30)

# Initialise variables which indicate state
recording = False  # "The camera is recording video"
camon = True  # "The camera is to stay on for the next cycle"

# Initialise stats
starttime = time()
recordstarttime = -1
recordfinishtime = -1
recordcount = 0
totalrecordtime = 0
captureinterval = 1
previouscapturetime = 0
capturecount = 0

# Main draw loop
while camon:
    # Capture image from camera
    ret, frame = cap.read()
    # If the frame was captured correctly
    if ret:
        # Converts from opencv image capture to pygame Surface
        pframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pframe = np.rot90(np.fliplr(pframe))
        # print(pframe.shape)
        pframe = pygame.surfarray.make_surface(pframe)
        # print(pframe.get_size())
        
        # Draw everything
        screen.fill(black)
        screen.blit(pframe, (0, 0))
        pygame.draw.line(screen, white, (640, 0), (640, h))
        if recording and time() > previouscapturetime + captureinterval:
            # Record frames if recording
            out.write(frame)
            # Show red recording circle
            pygame.draw.circle(screen, red, (15, 15), 10)
            # Update the potential end time of the recording
            recordfinishtime = time()
            previouscapturetime = recordfinishtime
            capturecount += 1
        # Generates the readout on the right
        messages = [["Activity this session:", green],
                    ["  Time: {}".format(HMS(time() - starttime)), green],
                    ["Recordings:", red],
                    ["  Time: {}".format(HMS(recordfinishtime - recordstarttime) if recordcount else None), red],
                    ["  Total: {}".format(HMS(totalrecordtime)), red],
                    ["  Count: {} videos".format(recordcount), red],
                    ["Captures:", blue],
                    ["  Every {} seconds".format(captureinterval), blue],
                    ["  Last: {}".format(HMS(previouscapturetime - recordstarttime) if recordcount else None), blue],
                    ["  Count: {}".format(capturecount), blue]]
        # Actually draws the readout
        for i, m in enumerate(messages):
            screen.blit(smallfont.render(m[0], True, m[1]), (650, 40 * i))
        # Draw everything to the display
        pygame.display.flip()
        
        # Event handling
        for e in pygame.event.get():
            # If window's x is pressed, prepare to leave
            if e.type == QUIT:
                camon = False
            elif e.type == KEYDOWN:
                # If spacebar is pressed, start or stop recording
                if e.key == K_SPACE:
                    if not recording:
                        recordcount += 1
                        out = cv2.VideoWriter("{}/{:.0f}.avi".format(path, time()), fourcc, 30, (640, 480))
                        recordstarttime = time()
                        previouscapturetime = recordstarttime
                    else:
                        out.release()
                        totalrecordtime += recordfinishtime - recordstarttime
                    recording = not recording
                # Increase or decrease interval with the up/down arrow keys
                if e.key == K_UP:
                    captureinterval += 0.5
                if e.key == K_DOWN:
                    captureinterval -= 0.5
                captureinterval = max(0.5, captureinterval)
                # If escape is pressed... as with the red x
                if e.key == K_ESCAPE:
                    camon = False

# Allow things to be gotten rid of, as necessary
cap.release()
if recording:
    out.release()
# cv2.destroyAllWindows()

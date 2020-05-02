import os
import time

FRAMES = 8700
TIMEBETWEEN = 900

frameCount = 0
while frameCount < FRAMES:
    imageNumber = str(frameCount).zfill(7)
    os.system("raspistill -vf -hf -o /home/pi/Desktop/Projekt/dhtWebServer/static/cam/cam%s.jpg"%(imageNumber))
    frameCount += 1
    time.sleep(TIMEBETWEEN - 6) #Takes roughly 6 seconds to take a picture
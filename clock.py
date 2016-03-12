#!/usr/bin/python

## @author Douglas Skrypa
## @version 1
## Date: 11/10/10

## Import classes required for display and calculations
from Tkinter import *;
import time;
import math;
## debugOn : True to display debug text; False to hide
debugOn = False;
## Static variables for calculations
toRADIAN = 3.14159 / 180;
faceWidth = 500;
faceHeight = 500;
a = faceWidth / 2.0;
b = faceHeight / 2.0;
## Create canvas
clock = Tk();
face = Canvas(clock, width=faceWidth, height=faceHeight);
face.pack();

## Starts the loop to display the clock.  Terminates on window close.
def run():
    try:
        drawBackground();
        clock.title("Python Analog Clock");
        while(True):
            drawFace();
            time.sleep(0.25);
    except:
        print "Clock stopped.";

## Draw the background of the clock
def drawBackground():
    face.create_oval(0, 0, 500, 500, fill="white", tag="clockFace");
    
    ## Draw lines around edge of clock
    faceTheta = 0;  
    while (faceTheta <= 360):
        fX = (a * 7/8) * math.cos(faceTheta * toRADIAN) + a;
        fY = (b * 7/8) * math.sin(faceTheta * toRADIAN) + b;
        fX2 = a * math.cos(faceTheta * toRADIAN) + a;
        fY2 = b * math.sin(faceTheta * toRADIAN) + b;

        fTag = "faceLine_"+str(faceTheta);
        face.create_line(fX, fY, fX2, fY2, tag=fTag);
        debug(fTag);
        faceTheta += 30;

## Draw hands on clock based on current system time
def drawFace():
    hour = float(time.strftime("%I"));
    minute = float(time.strftime("%M"));
    second = float(time.strftime("%S"));

    ## Calculate hour hand position
    degreesPerHour = 30;
    hourTheta = ((hour - 3) * degreesPerHour * toRADIAN) + ((minute * 0.5) * toRADIAN);
    hX = (a/2) * math.cos(hourTheta) + a;
    hY = (b/2) * math.sin(hourTheta) + b;

    ## Calculate minute hand position
    degreesPerMin = 6;
    minTheta = ((minute-15) * degreesPerMin) * toRADIAN;
    mX = (a * 3/4) * math.cos(minTheta) + a;
    mY = (b * 3/4) * math.sin(minTheta) + b;

    ## Calculate second hand position
    degreesPerSecond = 6;
    secTheta = ((second-15) * degreesPerSecond) * toRADIAN;
    sX = (a * 15/16) * math.cos(secTheta) + a;
    sY = (b * 15/16) * math.sin(secTheta) + b;

    ## Clean up old hand positions
    face.delete("hourHand");
    face.delete("minuteHand");
    face.delete("secondHand");

    ## Draw new hand positions    
    face.create_line(a, b, hX, hY, tag="hourHand");
    face.create_line(a, b, mX, mY, tag="minuteHand");
    face.create_line(a, b, sX, sY, tag="secondHand");

    debug(str(hour)+":"+str(minute)+":"+str(second)+" | Clock drawn.");
    face.update();    
    
## @param String x : String to be displayed when debug mode is set to on
def debug(x):
    if (debugOn):
        print "[Debug] "+x;

if __name__ == "__main__":
	run();
#/__main__

import numpy as np
import cv2
import time
from grabscreen import grab_screen
from keys import Keys

import playsound

HEIGTH = 768
WIDTH = 1024

keys = Keys()


def move_mouse(click_x,click_y):
    keys.keys_worker.sendMouse(dx=0, dy=0, buttons=keys.mouse_lb_press)
    time.sleep(1)
    # time.sleep(0.2)
    keys.keys_worker.sendMouse(dx=-1, dy=0, buttons=keys.mouse_lb_release)
    # time.sleep(0.2)

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

last_time = time.time()

DEBUG = 0
DEBUGwhiteGray = 1

toolDEBUG = 0

boolMoveMouse = 0
boolMoveSlowMouse = 0
boolMoveMouseShoot = 1

boolSlowFPS = 0

boolMat = 0
##24 ok
#18 ok pebkac and drunk
intSubdiv = 18
#bugfix missing last lines
iHEIGTH = (HEIGTH//intSubdiv)
iWIDTH = (WIDTH//intSubdiv)
#bugfix inverted width height
simpleMat = np.zeros((iHEIGTH,iWIDTH,1), np.uint8)

boolDisableMask = 0

img = np.zeros((50,400,3), np.uint8)

#TODO: Figuring out sursor position of blockade 3d

iCoin = 0


while (iCoin<50):
#while (True):

    screen = grab_screen(region=(0,0,WIDTH,HEIGTH))

    screenGray = cv2.cvtColor(screen,  cv2.COLOR_BGR2GRAY)

    #ret,whiteChannel = cv2.threshold(screenGray,28,255,cv2.THRESH_BINARY)
    ret,whiteChannel = cv2.threshold(screenGray,28,255,cv2.THRESH_BINARY)

    notADamnThing = ""
    iix = 0
    iiy = 0
    detectedX = 0
    detectedY = 0
    once = 0
    transWhiteChannel = whiteChannel.transpose()
    for lineX in simpleMat:
        #processing simplify matrix here
        for rowY in lineX:
            if(iiy < WIDTH):
                if(iix < 2):
                    if(transWhiteChannel[iiy][iix] == 255):
                        if(transWhiteChannel[0][0] == 0):
                            if(once == 0):
                                once = 1
                                detectedX = str(iix)
                                detectedY = str(iiy)
                        else:
                            print("top left corner achieved")
            iiy += 1
            #notADamnThing = notADamnThing + str(rowY)
        #notADamnThing = notADamnThing + '\n'
        #next line
        iix += 1

    if(once):
        move_mouse(int(detectedX),int(detectedY))


    #TODO:adding mouse pointing point here

    #print('{} FPS'.format( 1/(time.time()-last_time)))
    #print('{} msec'.format( (time.time()-last_time)*1000))
    print('{} FPS'.format( (1/(time.time()-last_time))))
    last_time = time.time()

    #cv2.imshow('windowSimpleMatrix',simpleMat)

    #cv2.imshow('windowWhite',whiteChannel)

    #my code here

    #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    iCoin += 1


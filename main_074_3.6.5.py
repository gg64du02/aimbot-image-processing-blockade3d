
import numpy as np
import cv2
import time
import pyautogui
from grabscreen import grab_screen
from keys import Keys

#import playsound

import keyboard


#multiprocessor
# from multiprocessing import Pool


# for stastical analisys
import matplotlib.pyplot as plt

# file name
import os

stats = []

st_total_time = time.time()

HEIGTH = 768
WIDTH = 1024

keys = Keys()

#tips for speed:
#use it from the windows explorer
#during the screengrab versuss the
#offset of the coordinates calculated for the aiming part

stopScript = False

# the first:BLUE?
# the second:GREEN
# the third:RED?
# yellow
# red [255   0   0]
# green [  0 255  0]
# blue [  0   0 255]
# dropped idea for now
def is_a_RelevantColor(tmpScreenRGBpixel):
    # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
    # red
    # if(tmpScreenRGBpixel[1] != 0 or tmpScreenRGBpixel[2] != 0):
    #     print("there:"+str(tmpScreenRGBpixel[1])+str(tmpScreenRGBpixel[2]))
    if((tmpScreenRGBpixel[0] == 255) and (tmpScreenRGBpixel[1] < 216) and (tmpScreenRGBpixel[2] < 216)):
        # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
        return True
    if((tmpScreenRGBpixel[0] < 216) and (tmpScreenRGBpixel[1] == 255) and (tmpScreenRGBpixel[2] < 216)):
        # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
        return True
    if((tmpScreenRGBpixel[0] < 216) and (tmpScreenRGBpixel[1] < 216) and (tmpScreenRGBpixel[2] == 255)):
        # print("tmpScreenRGBpixel:"+str(tmpScreenRGBpixel))
        return True
    return False

## 10 0 right
##-10 0 left
#   0 10 down
#   0 -10 up
def mouse_shoot(click_x,click_y):
    # directMouse
    # time.sleep(0.01)
    keys.directMouse(dx=click_x, dy=click_y, buttons=keys.mouse_lb_press)
    # time.sleep(0.01)
    keys.directMouse(dx=click_x, dy=click_y, buttons=keys.mouse_lb_release)

#use by the windows settings
def nothing(x):
    pass

def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, 255)
    masked = np.bitwise_and(img, mask)
    return masked

def roi_color(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, 255)
    np.set_printoptions(legacy=False)
    #extracting the first dimension
    a = np.dsplit(mask, 3)
    mask = np.dstack((a[0],a[0],a[0]))
    #applying the mask
    masked = np.bitwise_and(img, mask)
    return masked


# fillConvexPoly

def roi_fillConvexPoly(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillConvexPoly(mask, vertices, 255)
    masked = np.bitwise_and(img, mask)
    return masked


def multiproc_target_finding(x):
    # todo
    # time.sleep(1)
    # print("slept for 1 sec")
    print(str(x))
    return True

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

last_time = time.time()

DEBUG = 0
DEBUGwhiteGray = 1

toolDEBUG = 0

boolMoveMouse = 0
boolMoveSlowMouse = 0

boolMat = 0
##24 ok
#18 ok pebkac and drunk
# intSubdiv = 18
# intSubdiv = 18
# intSubdiv = 24 v65 
intSubdiv = 24
#bugfix missing last lines
iHEIGTH = (HEIGTH//intSubdiv)
iWIDTH = (WIDTH//intSubdiv)
#bugfix inverted width height
simpleMat = np.zeros((iHEIGTH,iWIDTH,1), np.uint8)

boolDisableMask = 0

img = np.zeros((50,400,3), np.uint8)
cv2.namedWindow('settings')
# create trackbars for color change
cv2.createTrackbar('0..255Low','settings',0,255,nothing)
cv2.createTrackbar('0..255High','settings',0,255,nothing)

#TODO: Figuring out sursor position of blockade 3d

# for the first time
detectedX = 0
detectedY = 0

while (stopScript == False):
    st_time =time.time()
    # cv2.imshow('settings',img)
    # numberSettingssLow = cv2.getTrackbarPos('0..255Low','settings')
    # numberSettingsHigh = cv2.getTrackbarPos('0..255High','settings')

    screen = grab_screen(region=(0,40,WIDTH,HEIGTH+40))

    #masking the UI
    # vertices = np.array([[200,700],[200,600],[10,600],[10,168],[970,168],[970,700]], np.int32)
    # vertices = np.array([[200,700],[200,600],[10,600],[10,168],[970,168],[970,700]], np.int32)
    # vertices = np.array([ [10, 168],[10, 700], [970, 168], [970, 700]], np.int32)#LOL
    vertices = np.array([[10, 168], [10, 700],  [970, 700],[970, 168]], np.int32)  # faster ?

	#10 970 first
    #168 700 second


    roi_st_time = time.time()

    if(boolDisableMask == 0):
        # screen = roi(screen, [vertices])
        # screen = roi_color(screen, [vertices])
        screen = roi_fillConvexPoly(screen, vertices)

    roi_ed_time = time.time()

    # print("roi:{}ms".format((roi_ed_time-roi_st_time)*1000))

    # class 'numpy.ndarray'
    # print(type(screen))
    screenGray = cv2.cvtColor(screen,  cv2.COLOR_BGR2GRAY)

    ret,whiteChannel = cv2.threshold(screenGray,28,255,cv2.THRESH_BINARY)

    notADamnThing = ""
    # iix = 0
    iix = 168
    iiy = 0
    once = 0

    # ===========================
    # Detecting a target
    # ===========================
    for lineX in simpleMat:
        #processing simplify matrix here
        if(once == 0):
            for rowY in lineX:
                if(iiy < WIDTH):
                    if(iix < HEIGTH):
                        if(whiteChannel[iix,iiy] == 255):
                            if(whiteChannel[iix + 1,iiy] == 255):
                                if(is_a_RelevantColor(screen[iix+1,iiy+1])):
                                # if(is_a_RelevantColor(screen[iix+intSubdiv,iiy+intSubdiv])):

                        # if(whiteChannel[iix][iiy] == 255):
                        #     if(whiteChannel[iix + 1][iiy] == 255):
                        #         if(is_a_RelevantColor(screen[iix+1][iiy+1])):
                                    # bug off target shoots
                                    detectedX = str(iix)
                                    # or detectedX = str(iix+1)
                                    detectedY = str(iiy)
                                    once = 1
                iiy += intSubdiv
                # notADamnThing = notADamnThing + str(rowY)
                # notADamnThing = notADamnThing + str(tmpScreen[iix][iiy])
            # notADamnThing = notADamnThing + '\n'
            iiy = 0
            #next line
            iix += intSubdiv


    #bug fix: mixed up axis
    Xoffset = int(detectedY) - int(pyautogui.position()[0])
    Xoffset = int(Xoffset / 5)
    # good at 10 fps w/ intSubdiv at 16
    # Xoffset = int(Xoffset / 5)

    #bug fix: mixed up axis
    Yoffset = int(detectedX) + 40 - int(pyautogui.position()[1])
    Yoffset = int(Yoffset / 5)
    # good at 10 fps w/ intSubdiv at 16
    # Yoffset = int(Yoffset / 5)

    if(once == 1):
        # mouse_shoot(int(Xoffset), int(Yoffset))

        # todo: add a trigger button
        if (keyboard.is_pressed('tab') == False):
            mouse_shoot(Xoffset, Yoffset)

        # playsound.playsound('C:/Users/jerome/Desktop/pythonBlockade3D/mp3/pew.mp3', True)

        # print("notADamnThing:\n" + notADamnThing)

        once = 0

        # print("detectedX:" + str(detectedX) +"\ndetectedY:" + str(detectedY) + "\n")
        #
        # print("pyautogui.position():"+str(pyautogui.position()))
        # print("Xoffset:"+str(Xoffset)+"\nYoffset:"+str(Yoffset))



    #cv2.imshow('windowSimpleMatrix',simpleMat)
    # cv2.imshow('windowWhite',whiteChannel)
    # cv2.imshow('screen',screen)
    # cv2.imshow('tmpScreen',tmpScreen)
    # cv2.imshow('simpleMat',simpleMat)


    # cv2.imshow('window2',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # https: // docs.opencv.org / 3.0 - beta / modules / imgproc / doc / drawing_functions.html?highlight = fillpoly  # fillconvexpoly


    #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if(keyboard.is_pressed('n')):


        stopScript = True
        cv2.destroyAllWindows()

        num_bins = 100
        # n, bins, patches = plt.hist(stats, num_bins, facecolor='blue', alpha=0.5)
        ed_total_time = time.time()
        n, bins, patches = plt.hist(stats, num_bins, facecolor='blue', alpha=0.5, label="intSubdiv:"+str(intSubdiv)+"|time(sec):"+str(ed_total_time-st_total_time)+"|"+os.path.basename(__file__))
        plt.legend()
        plt.show()

    # print("loop time :{}ms".format((time.time()-st_time)*1000))
    # here
    print('FPS:{}FPS'.format( (1/(time.time()-st_time))))
    # print(str(int((1/(time.time()-st_time)))))
    stats.extend([np.uint8((1/(time.time()-st_time)))])
    # print("============================================")
# n
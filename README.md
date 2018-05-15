# aimbot-image-processing-blockade3d

## What is it:

A script to aimbot at anyone and shoot anyone in Blockade 3D.

It is a script to process on the rendered image of the game while it is in window mode 1024*768,
it will shoot at anything that looks like remotely like an head.

## Why:

I learnt a little bit of python through this project. And wanted to explore what is possible with
static rules coding when it comes to image processing. Another project might follow using a
Machine Learning technology.

## What does it look like:

Actually it is more difficult to play with it than without it.

Don't hesitate to take a peek at each video as I was progressing in the development.

https://www.youtube.com/watch?v=0JrUKxCvSsE&list=PL4ftK5Ce2m_ZT_fHOl6UeiZ9gOrT6PlHu

My first attempt was (hilarious):

https://www.youtube.com/watch?v=PNkFDKUuN-g

## How to use it:

1.get the game in the 1024*768 resolution in window mode

2.grab the windows try to put onto the top left corner of your screen,
you must be able to still see the windows blue line for the windows on the left.

3.run the top_left_B3D_prep_4_aimbot*.py script then put your mouse
during the countdown onto the white bar of the game windows
(it might take up to 50sec tops, usually about 10seconds)

4.your game's windows is ready to run

5.join a game and disable chat (press ESC and toggle the button)

6. equip the m700 or crossbow as a main weapon (because they don't have flames)

7.Enjoy (the potential) aimbot (that could be)

Tips:

-N will stop the script.

-TAB will show you the scoreboard ingame and let's you use you mouse.

-Don't make it run for too long if you don't have much memory:
the script will collect stastitics about how fast the script is running and
show you the results at the end (everything is local, nothing on the internet)

-inside the script main*.py is a variable named: intSubdiv, this is attended to
speed up the processing by about a factor of intSubdiv^2 (intSubdiv*intSubdiv).
Best values I found so far are between 18-24 pixels. (allow for /324 to /576 
execution time per loop)


## How to work on it:

I used python 3.6.5 (x64) on windows 10.

Have those module installed:
numpy,
cv2,
time,
pyautogui,
keyboard,
matplotlib,
os

I have Blockade 3D installed on Steam. You will an easier steam if have a profile with the
 m700 or the crossbow.

Please read ideas inside the TODO.md


## Credits:

Thanks to Daniel (for the keys.py librairy and contructive critizism): 

https://github.com/daniel-kukiela

https://twitter.com/daniel_kukiela


And for Sentdex (for little bit of code (Region Of interest) and for inspiring me in the first place):

https://github.com/Sentdex

https://www.youtube.com/user/sentdex

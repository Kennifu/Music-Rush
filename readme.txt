Project Name: Music Rush

Description: An interactive rhythm game that uses any .wav file to generate a playable map that corresponds with the beats and pitches of the song.

How to Run:

1. Open TermProjectTest.py and run the file
2. Click Play
3. Choose your gamemode. (1 player or 2 players)
4. Select a song using 'Select another song'. The default .wav file displayed is fancy.wav
5. Click Play Now!

Objectives of the game:
Hit the yellow circles
Avoid the grey ones
Survive until the song is over
You have 5 Lives.

Commands:
1 player: 
P1 - Left and right arrow keys to move, SPACE bar to hit a circle
2 players: 
P1 - Left and right arrow keys to move, UP arrow to hit a circle
P2 - A and D keys, W key to hit a circle

#Note: The grey circles make you lose a life and automatically hurt you on contact.
       The yellow circles gives you points, but to get them, you need to eat them manually.


Libraries imported:
sys, time, pyaudio, aubio, pygame, random, numpy, tkinter
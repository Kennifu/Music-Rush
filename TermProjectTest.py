######################################################
# Note: You need a .wav file for this program to work.
# 
# Once you have one, press F3 and replace '.wav' with your
# own '______.wav' file
#
#
# Citations: 
# https://github.com/aubio/aubio/blob/master/python/demos/demo_tapthebeat.py
# https://www.pygame.org/docs/ref/draw.html
# http://blog.lukasperaza.com/getting-started-with-pygame/
# https://freesound.org/people/adammusic18/sounds/208871/ (bass.wav)
# https://freesound.org/people/lewis/sounds/15575/ (hurtSoud.wav)
#
#######################################################
import sys, time, pyaudio, aubio, pygame, random
import numpy as np
import tkinter as tk 
from tkinter import filedialog

class StartMenu(object):
    def __init__(self, width = 500, height = 700, fps = 60, title = 'Music Rush'):
        pygame.init()
        self.width = width 
        self.height = height 
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.backgroundImage = pygame.image.load('startMenu.png')

    def run(self):
        playing = True 
        while playing:
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 160 <= clickX <= 340:
                        # play button 
                        if 397 <= clickY <= 450:
                            playing = False
                            GameMode().run()
                        elif 487 <= clickY <= 540:
                            playing = False
                            Tutorial().run()
                        elif 577 <= clickY <= 630:
                            playing = False
                            pygame.quit()
        pygame.quit()

class Tutorial(object):
    def __init__(self, width = 500, height = 700, fps = 60):
        pygame.init()
        self.width = width 
        self.height = height 
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.backgroundImage = pygame.image.load('tutorialScreen.png')

    def run(self):
        playing = True 
        while playing:
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 150 <= clickX <= 350:
                        if 545 <= clickY <= 622:
                            playing = False
                            StartMenu().run()
        pygame.quit()

class GameMode(object):
    def __init__(self, width = 500, height = 700, fps = 60):
        pygame.init()
        self.width = width 
        self.height = height 
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.backgroundImage = pygame.image.load('gameMode.png')

    def run(self):
        playing = True 
        while playing:
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 30 <= clickX <= 472:
                        # play button 
                        if 265 <= clickY <= 415:
                            playing = False
                            SongSelect(1).run()
                        elif 465 <= clickY <= 615:
                            playing = False
                            SongSelect(2).run()
        pygame.quit()

class SongSelect(object):
    def __init__(self, players, width = 500, height = 700, fps = 60):
        self.filePath = 'fancy.wav'
        self.backgroundImage = pygame.image.load('songSelect.png')
        self.width = width
        self.height = height 
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.players = players
        pygame.font.init()
        pygame.init()

    def run(self):
        playing = True
        while playing:
            pygame.display.update()
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            pygame.font.init()
            self.printText(self.filePath)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    # play button 
                    if 140 <= clickX <= 377:
                        if 313 <= clickY <= 413:
                            if self.filePath.endswith('.wav'):
                                playing = False
                                self.textFile = self.getPathName(self.filePath)
                                self.leaderboard = open(self.textFile, 'a+')
                                self.leaderboard.close()
                                self.leaderboard = open(self.textFile, 'r')
                                self.highscore = self.leaderboard.read()
                                if self.highscore == '':
                                    self.leaderboard = open(self.textFile, 'a')
                                    self.leaderboard.write('0')
                                    self.leaderboard = open(self.textFile, 'r')
                                    self.highscore = self.leaderboard.read()
                                self.leaderboard.close()
                                if self.players == 1:
                                    MusicRush(self.filePath, self.highscore, self.textFile).run()
                                if self.players == 2:
                                    MusicRushMulti(self.filePath, self.highscore, self.textFile).run()
                    if 213 <= clickX <= 450:
                        if 584 <= clickY <= 613:
                            self.getFile()
        pygame.quit()

    def getFile(self):
        root = tk.Tk()
        root.withdraw()
        self.filePath = filedialog.askopenfilename()
        print(self.filePath)

    def printText(self, path):
        fileNameList = path.split('/')
        fileName = fileNameList[-1]
        nameLength = len(fileName)
        fontSize = min(450 // (nameLength + 1), 30)
        font = pygame.font.SysFont('consolas', fontSize)
        text = font.render(fileName, True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = 263
        textrect.centery = 538
        self.gameDisplay.blit(text, textrect)

    def getPathName(self, path):
        lenPath = len(path)
        fileName = path[:(lenPath-4)]
        return f'{fileName}.txt'

class MusicRush(object):
    def __init__(self, filename, highscore, textFile, width = 500, height = 700, fps = 60):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        hitSound = pygame.mixer.Sound('bass.wav')
        hurtSound = pygame.mixer.Sound('hurtSound.wav')
        width = width 
        height = height 
        fps = fps 
        filename = filename 
        highscore = highscore
        textFile = textFile
        player = Player(width, height)
        fftSize = 512 
        hopSize = fftSize // 2
        beats, onsets, pitches, audioTempo = audioSetup(
                                filename, fftSize, hopSize)
        bpms, bpmsChange = self.getChangeInTempo(beats)
        bpmsAvg = np.mean(bpms)
        enemiesList, lightsList, arcsList = createEnemies(beats, onsets, 
                                  pitches, bpms, width, height, 1)
        audioSource, stream = self.readFile(
                                filename, fftSize, hopSize)
        myfont = pygame.font.SysFont('impact', 30)
        screen = pygame.display.set_mode((width, height))
        fps = 60
        gameOver = False 
        accuracyList = [] 

    def pyaudio_callback(self, _in_data, _frame_count, _time_info, _status):
        samples, read = self.audioSource()
        isBeat = self.audioTempo(samples)
        audiobuf = samples.tobytes()
        if read < self.hopSize:
            return (audiobuf, pyaudio.paComplete)
        return (audiobuf, pyaudio.paContinue)
        # wait for the stream to finish. game ends when stream ends.

    def readFile(self, filename, fftSize, hopSize):
        fileName = filename
        self.sampleRate = 0 
        if len(sys.argv) > 2:
            sampleRate = int(sys.argv[2])
        self.audioSource = aubio.source(fileName, self.sampleRate, hopSize)
        self.sampleRate = 44100 
        self.audioTempo = aubio.tempo('default', self.fftSize, self.hopSize, self.sampleRate)
        self.audioPitch = aubio.pitch('default', self.fftSize, self.hopSize, self.sampleRate)
        self.audioOnset = aubio.onset('default', self.fftSize, self.hopSize, self.sampleRate)
        # create a simple click sound
        #click = 0.7 * np.sin(2. * np.pi * np.arange(hopSize) / hopSize * sampleRate / 3000)
        # create pyaudio stream with frames_per_buffer = hopSize and format = paFloat32
        p = pyaudio.PyAudio()
        pyaudio_format = pyaudio.paFloat32
        frames_per_buffer = self.hopSize 
        n_channels = 1 
        self.stream = p.open(format = pyaudio_format, channels = n_channels, rate = self.sampleRate,
                        output = True, frames_per_buffer = frames_per_buffer, 
                        stream_callback = self.pyaudio_callback)
        self.stream.start_stream()
        return self.audioSource, self.stream

    def timerFired(self, time, tempo):
        if time % 7 == 0:
            for enemy in self.enemiesList:
                if enemy.onScreen:
                    enemy.y += enemy.velocity
                    enemy.x += int(enemy.velocity * enemy.dx)
                    enemy.r = int(min(self.width//20,(self.width // 10 * ((enemy.y - 200)/ self.height))))
                    if touchingPlayer(self.player.x, self.player.y, self.player.r, 
                        enemy.x, enemy.y, enemy.r):
                        if isinstance(enemy, HurtfulEnemy):
                            self.hitSound.play()                        
                            enemy.y = self.height + 500
                            self.player.playerLives -= 1
                            self.hurtSound.play()
                            self.player.playerScore += enemy.reward 
                        # print(time, enemy.appearTime)
                        if self.player.playerLives == 0:
                            self.gameOver = True
            for lights in self.lightsList:
                if lights.onScreen:
                    lights.y += lights.velocity
                    lights.x += int(lights.velocity * lights.dx)
                    lights.r = int(self.width // 3 * ((lights.y - 200)/ self.height))
            for arcs in self.arcsList:
                if arcs.onScreen:
                    arcs.y += arcs.velocity
                    arcs.r = arcs.velocity * (arcs.y-200)

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        self._keys = dict()
        playing = True 
        playerScore = self.player.playerScore 
        samples, read = self.audioSource()
        tempo = self.bpms[1]
        self.stream.start_stream()
        timeElapsed = 0
        while playing:
            background = (0, 0, 0)
            timeElapsed += clock.get_time()
            screen.fill(background)
            scoreCount = self.myfont.render(f'Score: {self.player.playerScore}', False, (255, 255, 255))
            screen.blit(scoreCount, (5, 0))
            playerLives = self.myfont.render(f'Lives: {self.player.playerLives}', False, (255, 255, 255))
            screen.blit(playerLives, (5, 50))
            highScoreCount = self.myfont.render(f'Highscore: {self.highscore}', False, (255, 255, 255))
            screen.blit(highScoreCount, (5, 100))
            self.drawEnemy(screen, self.height, self.enemiesList, timeElapsed)
            self.drawMap(screen)
            self.drawPlayer(screen)
            self.drawLights(screen, self.lightsList, timeElapsed)
            self.drawArcs(screen, self.arcsList, timeElapsed)
            #edit here
            if timeElapsed in self.beats:
                index = self.beats.index(timeElapsed)
                tempo = self.bpms[index]
            self.timerFired(timeElapsed, tempo)
            if timeElapsed > self.enemiesList[-1].appearTime:
                playing = False
                WinScreen(self.player).run()
                break
            if self.gameOver == True:
                playing = False
                self.stream.stop_stream()
                GameOver().run()
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    self.stream.stop_stream()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.player.row > 0:
                            self.player.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        if self.player.row < 2:
                            self.player.moveRight()
                    elif event.key == pygame.K_SPACE:
                        for enemy in self.enemiesList:
                            if enemy.onScreen:
                                if touchingPlayer(self.player.x, self.player.y, self.player.r, 
                                    enemy.x, enemy.y, enemy.r):
                                    self.hitSound.play()       
                                    hitAccuracy = accuracy(self.player.x, self.player.y, self.player.r, 
                                    enemy.x, enemy.y, enemy.r)
                                    if hitAccuracy == 'Okay':
                                        self.player.playerScore += 10
                                    if hitAccuracy == 'Good':
                                        self.player.playerScore += 20
                                    if hitAccuracy == 'Excellent':
                                        self.player.playerScore += 30
                                    self.accuracyList.append(Accuracy(hitAccuracy, self.width, self.height))         
                                    enemy.y = self.height + 500              
            if len(self.accuracyList) > 0:
                    for text in self.accuracyList:
                        myText = self.myfont.render(f'{text.accuracy}', False, (255, 255, 255))
                        screen.blit(myText, (text.x, text.y))
                        if timeElapsed % 2 == 0:    
                            text.x -= text.velocity
                        if text.x < 0:
                            self.accuracyList.pop(0)

            if self.player.playerScore > int(self.highscore):
                self.highscore = str(self.player.playerScore)
                self.leaderboard = open(self.textFile, 'w+')
                self.leaderboard.write(self.highscore)
                self.leaderboard.close()
                self.leaderboard = open(self.textFile, 'r')
                contents = self.leaderboard.read()
                self.leaderboard.close()
            pygame.display.update()
            clock.tick()
        self.stream.close()
        pygame.quit()

    def getChangeInTempo(self, beats):
        bpms = [] # beats per millisecond, essentially the tempo
        for everyBeat in range(0, len(beats)):
            # finds bpms by finding the time between each beats
            bpms.append(max(beats[everyBeat] - beats[everyBeat - 1], 0))
        bpmsChange = [] 
        for beat in range(0, len(bpms)):
            # finds change in tempo 
            bpmsChange.append(max(bpms[beat] - bpms[beat - 1], 0))
        return bpms, bpmsChange

    def drawMap(self, surface):
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*0//3, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*1//3, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*2//3, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*3//3, self.height))

    def drawPlayer(self, surface):
        pygame.draw.circle(surface, self.player.color, (self.player.x, self.player.y), self.player.r) #Player

    def drawLights(self, surface, lightsList, timeElapsed):
        for lights in lightsList:
            x, y, r = lights.x, lights.y, lights.r
            angle = lights.angle
            starCoordList = [] 
            '''
            for i in range(10):
                if i % 2 == 0:
                    pointX, pointY = x + r*np.cos(angle + (2/5)*np.pi*(i/2)), y + r*np.sin(angle + (2/5)*np.pi*(i/2))
                    starCoordList.append((pointX, pointY))
                if i % 2 == 1:
                    pointX, pointY = x + r/3*np.cos(angle + (2/5)*np.pi*(i/2)), y + r/3*np.sin(angle + (2/5)*np.pi*(i/2))
                    starCoordList.append((pointX, pointY))
            '''
            if lights.y >= self.height:
                lights.onScreen = False
                lightsList.pop(0)
            elif lights.appearTime <= timeElapsed:
                lights.onScreen = True
                pygame.draw.circle(surface, lights.color, (lights.x, lights.y), lights.r)
                #pygame.draw.polygon(surface, lights.color, starCoordList)
            else:
                lights.onScreen = False

    def drawArcs(self, surface, arcsList, timeElapsed):
        for arcs in arcsList:
            if arcs.y >= self.height:
                arcs.onScreen = False
                arcsList.pop(0)
            elif arcs.appearTime <= timeElapsed:
                arcs.onScreen = True
                pygame.draw.arc(surface, arcs.color, 
                [arcs.x - max(arcs.r,4)/2, arcs.staticY - max(arcs.r,4)/2, 
                max(arcs.r,4), max(arcs.r,4)], 
                np.pi*3/2 + 0.45*np.arcsin(2/np.sqrt(5)), 
                np.pi*3/2 - 0.45*np.arcsin(2/np.sqrt(5)),
                max(2, (arcs.y - 200)//10))
            else:
                arcs.onScreen = False

    def drawEnemy(self, surface, height, enemiesList, timeElapsed):
        for enemy in enemiesList:
            if enemy.y >= height:
                enemy.onScreen = False
                enemy.seen = True
                enemiesList.pop(0)
            elif enemy.appearTime <= timeElapsed:
                enemy.onScreen = True
                pygame.draw.circle(surface, enemy.color, (enemy.x, enemy.y), enemy.r)
            else:
                enemy.onScreen = False

class MusicRushMulti(MusicRush):
    def __init__(self, filename, highscore, textFile, width = 500, height = 700, fps = 60):
        super().__init__(filename, highscore, textFile)
        self.player1 = Player1(self.width, self.height)
        self.player2 = Player2(self.width, self.height)
        self.p1Alive = True
        self.p2Alive = True
        self.enemiesList, self.lightsList, self.arcsList = createEnemies(self.beats, self.onsets, 
        self.pitches, self.bpms, self.width, self.height, 2)

    def timerFired(self, time, tempo):
        if time % 10 == 0:
            for enemy in self.enemiesList:
                if enemy.onScreen:
                    enemy.y += enemy.velocity * 1
                    enemy.x += int(enemy.velocity * enemy.dx)
                    enemy.r = int(min(self.width//20,(self.width // 10 * ((enemy.y - 200)/ self.height))))
                    if self.p1Alive:
                        if touchingPlayer(player1.x, player1.y, player1.r, 
                            enemy.x, enemy.y, enemy.r):
                            if isinstance(enemy, HurtfulEnemy):
                                self.hitSound.play()                        
                                enemy.y = self.height + 500
                                self.player1.playerLives -= 1
                                self.hurtSound.play()
                            # print(time, enemy.appearTime)
                            if self.player1.playerLives == 0:
                                self.p1Alive = False
                    if self.p2Alive:
                        if touchingPlayer(player2.x, player2.y, player2.r, 
                            enemy.x, enemy.y, enemy.r):
                            if isinstance(enemy, HurtfulEnemy):
                                self.hitSound.play()                        
                                enemy.y = self.height + 500
                                self.player2.playerLives -= 1
                                self.hurtSound.play()
                            # print(time, enemy.appearTime)
                            if self.player2.playerLives == 0:
                                self.p2Alive = False
                    if self.player1.playerLives == 0 and self.player2.playerLives == 0:
                            self.gameOver = True
            for lights in self.lightsList:
                if lights.onScreen:
                    lights.y += lights.velocity
                    lights.x += int(lights.velocity * lights.dx)
                    lights.r = int(self.width // 3 * ((lights.y - 200)/ self.height))
            for arcs in self.arcsList:
                if arcs.onScreen:
                    arcs.y += arcs.velocity
                    arcs.r = arcs.velocity * (arcs.y-200)

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        self._keys = dict()
        playing = True 
        playerScore = self.player1.playerScore
        samples, read = self.audioSource()
        tempo = self.bpms[1]
        self.stream.start_stream()
        timeElapsed = 0
        while playing:
            background = (0, 0, 0)
            timeElapsed += clock.get_time()
            screen.fill(background)
            scoreCount = self.myfont.render(f'Score: {self.player1.playerScore}', False, (255, 255, 255))
            screen.blit(scoreCount, (5, 0))
            player1Lives = self.myfont.render(f'P1 Lives: {self.player1.playerLives}', False, (255, 255, 255))
            screen.blit(player1Lives, (5, 50))
            player2Lives = self.myfont.render(f'P2 Lives: {self.player2.playerLives}', False, (255, 255, 255))
            screen.blit(player2Lives, (5, 100))
            highScoreCount = self.myfont.render(f'Highscore: {self.highscore}', False, (255, 255, 255))
            screen.blit(highScoreCount, (5, 150))
            self.drawEnemy(screen, self.height, self.enemiesList, timeElapsed)
            self.drawMap(screen)
            self.drawPlayer(screen)
            self.drawLights(screen, self.lightsList, timeElapsed)
            self.drawArcs(screen, self.arcsList, timeElapsed)
            #edit here
            if timeElapsed in self.beats:
                index = self.beats.index(timeElapsed)
                tempo = self.bpms[index]
            self.timerFired(timeElapsed, tempo)
            if timeElapsed > self.enemiesList[-1].appearTime:
                playing = False
                WinScreen2(self.player1, self.player2).run()
                break
            if self.gameOver == True:
                playing = False
                self.stream.stop_stream()
                GameOver().run()
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    self.stream.stop_stream()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if player1.row > 0:
                            player1.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        if player1.row < 4:
                            player1.moveRight()
                    if event.key == pygame.K_a:
                        if player2.row > 0:
                            player2.moveLeft()
                    elif event.key == pygame.K_d:
                        if player2.row < 4:
                            player2.moveRight()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        for enemy in self.enemiesList:
                            if enemy.onScreen:
                                if touchingPlayer(player1.x, player1.y, player1.r, 
                                    enemy.x, enemy.y, enemy.r):
                                    self.hitSound.play()       
                                    hitAccuracy = accuracy(player1.x, player1.y, player1.r, 
                                    enemy.x, enemy.y, enemy.r)
                                    if hitAccuracy == 'Okay':
                                        self.player1.playerScore += 10
                                    if hitAccuracy == 'Good':
                                        self.player1.playerScore += 20
                                    if hitAccuracy == 'Excellent':
                                        self.player1.playerScore += 30
                                    self.accuracyList.append(Accuracy(hitAccuracy, self.width, self.height))         
                                    enemy.y = self.height + 500  
                                if touchingPlayer(player2.x, player2.y, player2.r, 
                                    enemy.x, enemy.y, enemy.r):
                                    self.hitSound.play()       
                                    hitAccuracy = accuracy(player2.x, player2.y, player2.r, 
                                    enemy.x, enemy.y, enemy.r)
                                    if hitAccuracy == 'Okay':
                                        self.player1.playerScore += 10
                                    if hitAccuracy == 'Good':
                                        self.player1.playerScore += 20
                                    if hitAccuracy == 'Excellent':
                                        self.player1.playerScore += 30
                                    self.accuracyList.append(Accuracy(hitAccuracy, self.width, self.height))         
                                    enemy.y = self.height + 500        
                                          
            if len(self.accuracyList) > 0:
                    for text in self.accuracyList:
                        myText = self.myfont.render(f'{text.accuracy}', False, (255, 255, 255))
                        screen.blit(myText, (text.x, text.y))
                        if timeElapsed % 2 == 0:    
                            text.x -= text.velocity
                        if text.x < 0:
                            self.accuracyList.pop(0)

            if self.player1.playerScore > int(self.highscore):
                self.highscore = str(self.player1.playerScore)
                self.leaderboard = open(self.textFile, 'w+')
                self.leaderboard.write(self.highscore)
                self.leaderboard.close()
                self.leaderboard = open(self.textFile, 'r')
                contents = self.leaderboard.read()
                self.leaderboard.close()
            pygame.display.update()
            clock.tick()
        self.stream.close()
        pygame.quit()

    def drawMap(self, surface):
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*0//5, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*1//5, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*2//5, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*3//5, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*4//5, self.height))
        pygame.draw.line(surface, (119, 184, 249), (self.width//2, 200), (self.width*5//5, self.height))

    def drawPlayer(self, surface):
        if self.p1Alive:
            pygame.draw.circle(surface, player1.color, (player1.x, player1.y), player1.r) #Player
        if self.p2Alive:
            pygame.draw.circle(surface, player2.color, (player2.x, player2.y), player2.r) #Player2

class GameOver(object):
    def __init__(self, width = 500, height = 700, fps = 60):
        pygame.init()
        self.width = width 
        self.height = height 
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.backgroundImage = pygame.image.load('gameOver.png')

    def run(self):
        playing = True 
        while playing:
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 132 <= clickX <= 369:
                        # play button 
                        if 391 <= clickY <= 493:
                            playing = False
                            StartMenu().run()
                        elif 533 <= clickY <= 588:
                            playing = False
                            pygame.quit()
        pygame.quit()

class WinScreen(object):
    def __init__(self, player, width = 500, height = 700, fps = 60):
        pygame.init()
        self.player = player
        self.width = width 
        self.height = height 
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.backgroundImage = pygame.image.load('winScreen.png')
        self.myfont = pygame.font.SysFont('impact', 30)

    def run(self):
        playing = True 
        while playing:
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            playerStats = self.myfont.render('Here are your stats', False, (255, 255, 255))
            self.gameDisplay.blit(playerStats, (70, 183))
            scoreCount = self.myfont.render(f'Score: {self.player.playerScore}', False, (255, 255, 255))
            self.gameDisplay.blit(scoreCount, (70, 233))
            playerLives = self.myfont.render(f'Lives: {self.player.playerLives}', False, (255, 255, 255))
            self.gameDisplay.blit(playerLives, (70, 283))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 133 <= clickX <= 369:
                        if 560 <= clickY <= 615:
                            playing = False
                            pygame.quit()
                            break
        pygame.quit()

class WinScreen2(WinScreen):
    def __init__(self, player, player2, width = 500, height = 700, fps = 60):
        super().__init__(player)
        self.player2 = player2

    def run(self):
        playing = True 
        while playing:
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
            playerStats = self.myfont.render('Here are your stats', False, (255, 255, 255))
            self.gameDisplay.blit(playerStats, (70, 183))
            scoreCount = self.myfont.render(f'Combined Score: {self.player.playerScore}', False, (255, 255, 255))
            self.gameDisplay.blit(scoreCount, (70, 233))
            playerLives = self.myfont.render(f'P1 Lives: {self.player.playerLives}', False, (255, 255, 255))
            self.gameDisplay.blit(playerLives, (70, 283))
            player2Lives = self.myfont.render(f'P2 Lives: {self.player2.playerLives}', False, (255, 255, 255))
            self.gameDisplay.blit(player2Lives, (70, 333))            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickX, clickY = event.pos
                    if 133 <= clickX <= 369:
                        if 560 <= clickY <= 615:
                            playing = False
                            pygame.quit()
                            break
        pygame.quit()

class Player(object):
    def __init__(self, width, height):
        self.row = 1 #Always start in the middle row (three rows)
        self.x = width//2
        self.y = height*9//10
        self.r = width//20 
        self.color = (119, 184, 249) 
        self.playerScore = 0
        self.width = width 
        self.height = height
        self.playerLives = 5

    def moveLeft(self):
        self.row -= 1 
        self.x -= (self.width//3 - 20)
    def moveRight(self):
        self.row += 1 
        self.x += (self.width//3 - 20)

class Player1(Player):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.row = 3
        self.color = (119, 184, 249)
        self.x = width//2 + (self.width//5 - 10)

    def moveLeft(self):
        self.row -= 1 
        self.x -= (self.width//5 - 10)
    def moveRight(self):
        self.row += 1 
        self.x += (self.width//5 - 10)

class Player2(Player1):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.color = (77, 255, 131) 
        self.row = 1
        self.x = width//2 - (self.width//5 - 10)

class Enemy(object):
    def __init__(self, beatTime, width, height, players):
        if players == 1:
            self.row = random.randint(0,2)
            if self.row == 0:
                self.dx = -1/3
            elif self.row == 1:
                self.dx = 0
            elif self.row == 2:
                self.dx = 1/3
            self.velocity = 3
        elif players == 2:
            self.row = random.randint(0,4)
            if self.row == 0:
                self.dx = -2/5
            elif self.row == 1:
                self.dx = -1/5
            elif self.row == 2:
                self.dx = 0
            elif self.row == 3:
                self.dx = 1/5
            elif self.row == 4:
                self.dx = 2/5
            self.velocity = 5
        self.x = width // 2
        self.y = 200
        self.r = int(width // 20 * (self.y / height))
        self.color = (255, 255, 0)
        self.onScreen = False
        self.seen = False
        self.reward = 100
        self.appearTime = beatTime - (height // self.velocity) * 2

class HurtfulEnemy(Enemy):
    def __init__(self, beatTime, width, height, players):
        super().__init__(beatTime, width, height, players)
        self.color = (125, 125, 125)
        self.reward = 0 

class BackgroundLights(object):
    #pitch to color converter, I will change the algorithm as I go. 
    @staticmethod
    def convertToColor(pitch, maxPitch, minPitch):
        colorRange = 255**3
        pitchRange = maxPitch - minPitch
        colorScale = colorRange // pitchRange
        if pitch <= minPitch + pitchRange * 1// 6: 
            return (255, int(255*pitch/pitchRange), 0)
        if pitch <= minPitch + pitchRange * 2 // 6:
            return (255 - int(255*pitch/pitchRange), 255, 0)
        if pitch <= minPitch + pitchRange * 3 // 6:
            return (0, 255, int(255*pitch/pitchRange))
        if pitch <= minPitch + pitchRange * 4 // 6:
            return (0, 255 - int(255*pitch/pitchRange), 255)
        if pitch <= minPitch + pitchRange * 5 // 6:
            return (int(255*pitch/pitchRange), 0, 255)
        if pitch <= minPitch + pitchRange * 6 // 6:
            return (255, 0, abs(255-int(255*pitch/pitchRange)))
        if pitch <= minPitch:
            return (0, 255, 0)
        if pitch >= minPitch + pitchRange * 6 // 6:
            return (255, 0, 0)

    def __init__(self, pitch, tempo, width, maxPitch, minPitch, bpms):
        self.x = width // 2
        self.y = 200
        self.r = 0 
        self.dx = random.choice([random.uniform(1, 3), random.uniform(-1, -3)])
        self.color = BackgroundLights.convertToColor(pitch, maxPitch, minPitch)
        self.velocity = max(bpms//100, 5)
        self.onScreen = False
        self.appearTime = tempo
        self.angle = random.uniform(0, np.pi/2)

class BackgroundArcs(BackgroundLights):
    def __init__(self, pitch, tempo, width, maxPitch, minPitch, bpms):
        super().__init__(pitch, tempo, width, maxPitch, minPitch, bpms)
        self.velocity = 5
        self.x = width//2
        self.y = 200 
        self.staticY = self.y

class Accuracy(object):
    def __init__(self, accuracy, width, height):
        self.x = width
        self.y = random.randint(0, height)
        self.accuracy = accuracy 
        self.velocity = 1

def audioSetup(filename, fftSize, hopSize):
    fftSize = fftSize 
    hopSize = hopSize
    fileName = filename
    sampleRate = 0 
    if len(sys.argv) > 2:
        sampleRate = int(sys.argv[2])
    audioSource = aubio.source(fileName, sampleRate, hopSize)
    sampleRate = audioSource.samplerate 
    audioTempo = aubio.tempo('default', fftSize, hopSize, sampleRate)
    audioPitch = aubio.pitch('default', fftSize, hopSize, sampleRate)
    audioOnset = aubio.onset('default', fftSize, hopSize, sampleRate)
    audioDelay = 4 * hopSize
    # list of beats, in saples
    beats = [] 
    onsets = []
    pitches = []
    # finds where all the beats are in the file
    totalFrames = 0 
    while True:
        samples, read = audioSource()
        isBeat = audioTempo(samples)
        isOnset = audioOnset(samples)
        if isBeat:
            thisBeat = int(totalFrames - audioDelay + isBeat[0] * hopSize)
            beats.append(int(thisBeat * 1000 / float(sampleRate)))
            pitches.append(audioPitch(samples)[0])
        if isOnset:
            thisOnset = int(totalFrames - audioDelay + isOnset[0] * hopSize)
            onsets.append(audioPitch(samples)[0])
        totalFrames += read 
        if read < hopSize: 
            break 
    return (beats, onsets, pitches, audioTempo)


def touchingPlayer(playerX, playerY, playerR, otherX, otherY, otherR):
    distance = ((otherX - playerX)**2 + (otherY - playerY)**2)**0.5
    hitboxSum = playerR + otherR 
    return distance <= hitboxSum

def accuracy(playerX, playerY, playerR, otherX, otherY, otherR):
    #print(playerX, playerY, playerR, otherX, otherY, otherR)
    centerDistance = ((otherX - playerX)**2 + (otherY - playerY)**2)**0.5
    #print(centerDistance, playerR)
    if centerDistance <= playerR//2:
        return 'Excellent'
    elif centerDistance <= playerR:
        return 'Good'
    else:
        return 'Okay'


# Complex part of the program, this data will be used to convert sounds to color.
def createEnemies(beats, onsets, pitches, bpms, width, height, players):
    enemiesList = [] 
    lightsList = [] 
    arcsList = []
    avgPitch = np.mean(pitches)
    stdPitch = np.std(pitches)
    maxPitch = (avgPitch + 1*stdPitch)
    minPitch = (avgPitch - 2*stdPitch)
    # Algorithm for creating the enemy and all the flashy background lights
    for numBeats in range(len(beats)):
        # We give each light and obstacle their 'time' in the same to show up 
        lightsList.append(BackgroundLights(pitches[numBeats], 
        beats[numBeats], width, maxPitch, minPitch, bpms[numBeats]))
        arcsList.append(BackgroundArcs(pitches[numBeats], 
        beats[numBeats], width, maxPitch, minPitch, bpms[numBeats]))
        if avgPitch - 0.25*stdPitch <= pitches[numBeats] <= avgPitch + 0.25*stdPitch:
            enemiesList.append(HurtfulEnemy(beats[numBeats], width, height, players))
        else:
            enemiesList.append(Enemy(beats[numBeats], width, height, players))
        if players == 2:
            if (pitches[numBeats] <= avgPitch - 2*stdPitch or 
                pitches[numBeats] >= avgPitch + 2*stdPitch):
                enemiesList.append(Enemy(beats[numBeats], width, height, players))
    return enemiesList, lightsList, arcsList

def main():
    player = Player(500, 700)
    player1 = Player1(500, 700)
    player2 = Player2(500, 700)
    StartMenu().run()

if __name__ == '__main__':
    main()
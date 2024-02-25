
import random, pygame, sys
from pygame.locals import *
import time

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

INDIANRED = (139,58,58)
INDIANRED2 =     (255,106,106)


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    global BLINK_STATUS
    BLINK_STATUS = True

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    direction = RIGHT

    #koordinati za vtoriot crv
    secondWormCoordinates = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    secondWormDirection = RIGHT
    secondWormVisibility = False
    startTime = time.time()

    # Start the apple in a random place.
    apple = getRandomLocation()

    #trepkacki objekti
    object1_location = None
    object1_timer = time.time()
    status1 = True
    object2_location = None
    object2_timer = time.time()
    status2 = True

    score = 0

    while True: # main game loop
        #da se pojavi crvot po 20 sekundi
        if time.time() - startTime >= 20:
            secondWormVisibility = True


        #vtoro baranje
        if time.time() - object1_timer >= 5:
            object1_timer = time.time() + 5
            object1_location = getRandomLocation()
        if time.time() - object2_timer >= 7:
            object2_timer = time.time() + 7
            object2_location = getRandomLocation()

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        grow = False

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            grow = True
        # else:
        #     del wormCoords[-1] # remove worm's tail segment

        #dali crvot kje izede nekoj od objektite
        if not object1_location is None:
            if wormCoords[HEAD]['x'] == object1_location['x'] and wormCoords[HEAD]['y'] == object1_location['y']:
                # object 1
                object1_timer = time.time() + 5
                score += 3
                object1_location = None
        if not object2_location is None:
            if wormCoords[HEAD]['x'] == object2_location['x'] and wormCoords[HEAD]['y'] == object2_location['y']:
                # object 2
                object2_timer = time.time() + 7
                score += 3
                object2_location = None

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        #noviot crv
        if secondWormVisibility:
            enemyWormGrowth = False
            xSecond = secondWormCoordinates[0]['x']
            ySecond = secondWormCoordinates[0]['y']
            possibles = [UP, DOWN, LEFT, RIGHT]
            if secondWormDirection == LEFT or xSecond >= CELLWIDTH - 1:
                possibles.remove(RIGHT)
            if secondWormDirection == RIGHT or xSecond <= 0:
                possibles.remove(LEFT)
            if secondWormDirection == UP or ySecond >= CELLHEIGHT - 1:
                possibles.remove(DOWN)
            if secondWormDirection == DOWN or ySecond <= 0:
                possibles.remove(UP)
            secondWormDirection = random.choice(possibles)
            if secondWormDirection == UP:
                secondHead = {'x': secondWormCoordinates[HEAD]['x'], 'y': secondWormCoordinates[HEAD]['y'] - 1}
            elif secondWormDirection == DOWN:
                secondHead = {'x': secondWormCoordinates[HEAD]['x'], 'y': secondWormCoordinates[HEAD]['y'] + 1}
            elif secondWormDirection == LEFT:
                secondHead = {'x': secondWormCoordinates[HEAD]['x'] - 1, 'y': secondWormCoordinates[HEAD]['y']}
            elif secondWormDirection == RIGHT:
                secondHead = {'x': secondWormCoordinates[HEAD]['x'] + 1, 'y': secondWormCoordinates[HEAD]['y']}
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                    return # крај на играта
            if secondWormCoordinates[HEAD] in wormCoords:
                enemyWormGrowth = True
            if wormCoords[HEAD] in secondWormCoordinates:
                grow = True
            if not enemyWormGrowth:
                del(secondWormCoordinates[-1])
            secondWormCoordinates.insert(0, secondHead)

        if not grow:
            del wormCoords[-1] # remove worm's tail segment

        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)

        #crtanje nov crv
        if secondWormVisibility:
            drawWorm(secondWormCoordinates, INDIANRED, INDIANRED2)

        #crtanje na objektite
        if object1_location is not None:
            drawObject(object1_location, INDIANRED, INDIANRED2, status1)
            status1 = not status1
        if object2_location is not None:
            drawObject(object2_location, INDIANRED, INDIANRED2, status2)
            status2 = not status2

        drawScore(len(wormCoords) - 3 + score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()

#funkcija za iscrtuvanje na objektite
def drawObject(coord, blinkColor, notBlinkColor, BLINK_STATUS=None):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    blinkingObjectRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    if BLINK_STATUS:
        pygame.draw.rect(DISPLAYSURF, blinkColor, blinkingObjectRect)
    else:
        pygame.draw.rect(DISPLAYSURF, notBlinkColor, blinkingObjectRect)


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

#createText funkcija
def createText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    # креирање на копчињата
    resetSurf, resetRect = createText('Start from the beginning', WHITE, GREEN, WINDOWWIDTH - 220, WINDOWHEIGHT - 120)
    quitSurf, quitRect = createText('Quit', WHITE, RED, WINDOWWIDTH - 140, WINDOWHEIGHT - 90)
    DISPLAYSURF.blit(resetSurf, resetRect)
    DISPLAYSURF.blit(quitSurf, quitRect)

    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        #klik na maus
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if resetRect.collidepoint(pos):
                    return
                if quitRect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


#promena
def drawWorm(wormCoords, borderColor = DARKGREEN, color = GREEN):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, borderColor, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
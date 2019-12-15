import pygame
import Constants
import Utils
import random
import GameObjectLoader
from collections import deque
from GameObject import GameObject
from Bird import Bird
from Network import Network
from GeneticAlgorithm import GeneticAlgorithm

def displayGameObject(window, gameObject):
    loadedImage = pygame.image.load(gameObject.imagePath)
    coordinates = (gameObject.xCoordinate,gameObject.yCoordinate)
    window.blit( loadedImage, coordinates)

def updateCoordinates(pipes, vel):
    for i in range(0, len(pipes)):
        northPipe, southPipe = pipes[i]
        
        northPipe.xCoordinate -= vel 
        southPipe.xCoordinate -= vel

def removeCoordinatesToLeftOfWindow(pipes, pipeWidth):
    while len(pipes) > 0:
        northPipe, _ = pipes[0]        
        if northPipe.xCoordinate < 0:
            northPipe.delImage()
            pipes.popleft()
            continue
        break    
    return pipes

def generateNewPipePair(pipeXCoordinate, northPipeHeight, groundYCoordinate, pipeWidth, gapBetweenPipes):    
    # generate north pipe
    newNorthPipeX = pipeXCoordinate
    newNorthPipeY = 0
    newNorthPipeWidth = pipeWidth
    newNorthPipeHeight = northPipeHeight
    newNorthPipe = GameObject(newNorthPipeX, newNorthPipeY, 
                              newNorthPipeWidth, newNorthPipeHeight,
                              Constants.BASE_PATH, Constants.PIPE_NORTH_NAME)

    # generate south pipe
    newSouthPipeX = pipeXCoordinate
    newSouthPipeY = newNorthPipeHeight + gapBetweenPipes
    newSouthPipeWidth = pipeWidth
    newSouthPipeHeight = groundYCoordinate - (gapBetweenPipes + newNorthPipeHeight)  
    newSouthPipe = GameObject(newSouthPipeX, newSouthPipeY, 
                              newSouthPipeWidth, newSouthPipeHeight,
                              Constants.BASE_PATH, Constants.PIPE_SOUTH_NAME)

    return (newNorthPipe, newSouthPipe)

def initializePipes(pipes):
    for i in range(0,len(Constants.INITIAL_NORTH_PIPES_X)):
        newPipePairs = generateNewPipePair(Constants.INITIAL_NORTH_PIPES_X[i],
                                           Constants.INITIAL_NORTH_PIPES_HEIGHT[i],
                                           Constants.GROUND_Y_COORDINATE,
                                           Constants.PIPE_WIDTH,
                                           Constants.GAP_BETWEEN_PIPES)
        pipes.append(newPipePairs)

def initGame():
    ##### load objects #####
    # load background
    global background 
    background = GameObject(0, 0, Constants.WINDOW_SIZE_WIDTH,Constants.WINDOW_SIZE_HEIGHT, Constants.BASE_PATH, Constants.BACKGROUND_IMAGE_NAME)

    global birds
    birds = [Bird(200,200,-1,-1,Constants.BASE_PATH, Constants.BIRD_IMAGE_NAME) for i in range(0, Constants.MAX_POPULATION_SIZE)]
    global flyingBirds
    flyingBirds = [Bird(200,200,-1,-1,Constants.BASE_PATH, Constants.FLYING_BIRD_IMAGE_NAME) for i in range(0, Constants.MAX_POPULATION_SIZE)]

    global pipes 
    pipes = deque()
    initializePipes(pipes)

    global playIsOn 
    playIsOn = True
    
    global iterationNumber 
    iterationNumber = 0

    global geneticAlgorithm
    geneticAlgorithm = GeneticAlgorithm(birds, Constants.GENETIC_ALGORITHM_NUMBER_OF_SELECTIONS,\
                                        Constants.CROSSOVER_RATE, Constants.MUTATION_RATE, \
                                        Constants.MUTATION_STRENGTH)

pygame.init()
pygame.font.init()

##### set display window and text ######
window = pygame.display.set_mode((Constants.WINDOW_SIZE_WIDTH, 
                                  Constants.WINDOW_SIZE_HEIGHT))
pygame.display.set_caption(Constants.WINDOW_DISPLAY_TEXT)

#### fonts ###
# define the RGB value for white, 
#  green, blue colour . 
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128)
gameOverTextFont = pygame.font.Font(Constants.EIGHT_BIT_MADNESS_FILE, 40)
scoreAfterGameOverTextFont = pygame.font.Font(Constants.EIGHT_BIT_MADNESS_FILE, 40)
scoreTextFont = pygame.font.Font(Constants.EIGHT_BIT_MADNESS_FILE, 65)

background = None
birds = None
flyingBirds = None
pipes = None
playIsOn = None
iterationNumber = None
geneticAlgorithm = None
pipesCrossed = 0

initGame()

while True:

    iterationNumber += 1

    if iterationNumber % 10 == 0:
        birds = geneticAlgorithm.evolve()
        flyingBirds = [Bird(bird.xCoordinate, bird.yCoordinate, bird.objectWidth, bird.objectHeight, bird.imageBasePath, Constants.FLYING_BIRD_IMAGE_NAME ) for bird in birds]

    pygame.time.delay(Constants.UPDATE_WINDOW_TIME)

    for i in range(0, len(birds)):
        bird = birds[i]
        flyingBird = flyingBirds[i]
        bird.recalculateFeatures(pipes)
        networkOutput = bird.networkForwardStep()
        if networkOutput[0] > 0.5:
            bird.jump = Constants.JUMP_DISTANCE
            bird.isJump = True
        if bird.isJump:
            if bird.jump >= -1 * Constants.JUMP_DISTANCE:

                neg = 1
                if bird.jump < 0:
                    neg = -1

                bird.changeCoordinate(-1 * ( bird.jump ** 2 ) * 0.600 * neg)
                bird.jump -= 1

            else:
                bird.jump = Constants.JUMP_DISTANCE
                bird.isJump = False
                bird.changeCoordinate(Constants.GRAVITY_FALL_DISTANCE)
        else:
            bird.changeCoordinate(Constants.GRAVITY_FALL_DISTANCE)
        
        if bird.isJump:
            flyingBird.xCoordinate = bird.xCoordinate
            flyingBird.yCoordinate = bird.yCoordinate
            flyingBird.display(window)
        else:
            bird.display(window)

    while len(pipes) < 10:
        newNorthPipeHeight = random.randint(Constants.MIN_HEIGHT_OF_PIPE, 
                                Constants.GROUND_Y_COORDINATE-(Constants.MIN_HEIGHT_OF_PIPE+Constants.GAP_BETWEEN_PIPES))
        newSouthPipeHeight = Constants.GROUND_Y_COORDINATE - (Constants.GAP_BETWEEN_PIPES + newNorthPipeHeight)

        latestNorthPipe, _ = pipes[-1]
        latestPipeX = latestNorthPipe.xCoordinate
        
        pipes.append(generateNewPipePair(latestPipeX + Constants.NEXT_PIPE_ADDITION_GAP,
                                            newNorthPipeHeight,
                                            Constants.GROUND_Y_COORDINATE,
                                            Constants.PIPE_WIDTH,
                                            Constants.GAP_BETWEEN_PIPES))

    background.display(window)

    updateCoordinates(pipes, Constants.VELOCITY_OF_PIPES)
    removeCoordinatesToLeftOfWindow(pipes, Constants.PIPE_WIDTH)

    for northPipe, southPipe in pipes:            
        if northPipe.xCoordinate >= 0 & northPipe.xCoordinate < 500:

            northPipe.display(window)
            southPipe.display(window)

            pipeCrossedFlag = False
            for i in range(0, len(birds)):
                bird = birds[i]
                flyingBird = flyingBirds[i]

                if bird.alive == False:
                    continue

                isCollision = False
                # Check for collisions
                if not isCollision:
                    if bird.isJump:
                        isCollision = Utils.isCollision(flyingBird, northPipe, southPipe, Constants.BIRD_Y_COORDINATE_MIN, Constants.BIRD_Y_COORDINATE_MAX)
                    else:
                        isCollision = Utils.isCollision(bird, northPipe, southPipe, Constants.BIRD_Y_COORDINATE_MIN, Constants.BIRD_Y_COORDINATE_MAX)
            
                if isCollision:
                    bird.health -= 1

                if bird.health <= 0:
                    bird.alive = False
                    continue

                # Increment score
                if (northPipe.xCoordinate + Constants.PIPE_WIDTH) <=  bird.xCoordinate and \
                   (northPipe.xCoordinate + Constants.PIPE_WIDTH) >= (bird.xCoordinate - Constants.GAP_TO_COUNT_SCORE) and \
                   not(bird.lastPipeCrossed is northPipe):
                    bird.lastPipeCrossed = northPipe
                    if pipeCrossedFlag == False:
                        pipeCrossedFlag = True
                        pipesCrossed += 1
                    bird.score += 1
        else:
            break

    fittestBirdScore = 0 if len(birds) == 0 else max(bird.health for bird in birds)
    fittestBird = None
    aliveBirdsCount = 0
    birdYCordinate = 0
    overlappingBirds = dict()
    for i in range(0,len(birds)):
        if not bird.alive:
            continue
        aliveBirdsCount += 1
        bird = birds[i]
        flyingBird = flyingBirds[i]
        if bird.yCoordinate in overlappingBirds:
            overlappingBirds[bird.yCoordinate] += 1
        else:
            overlappingBirds[bird.yCoordinate] = 0 
        if ( bird.getFitness() == fittestBirdScore ):
            fittestBird = bird
        bird.display(window)
        if bird.yCoordinate != birdYCordinate:
            birdYCordinate = bird.yCoordinate
    
    print("alive: " + str(aliveBirdsCount))
    scoreText = scoreAfterGameOverTextFont.render('Score: ' + str(pipesCrossed), False, blue)
    window.blit(scoreText, (160, 85))

    if pipesCrossed == 999:
        # ITS ENOUGH NOW
        birds[0].saveObject(Constants.FITTEST_BIRD_PICKLE_FILE)
        break

    pygame.display.update()

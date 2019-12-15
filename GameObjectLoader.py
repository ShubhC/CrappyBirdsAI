import Constants
import Utils
import pygame
import uuid

def loadBackground(windowWidth, windowHeight):
    backgroundImageName = Utils.resizeImage(Constants.BASE_PATH,
                                            Constants.BACKGROUND_IMAGE_NAME,
                                            windowWidth,
                                            windowHeight)
    background = pygame.image.load(backgroundImageName)
    return background

def loadBird():
    birdImageName = Constants.BASE_PATH + Constants.BIRD_IMAGE_NAME
    bird = pygame.image.load(birdImageName)
    return bird

def loadNorthPipe(pipeWidth, pipeHeight):
    loadedImageName = Utils.getUuid();
    pipeNorthImageName = Utils.resizeImage(Constants.BASE_PATH,
                                           Constants.PIPE_NORTH_NAME,
                                           loadedImageName,
                                           pipeWidth,
                                           pipeHeight)
    return loadedImageName

def loadSouthPipe(pipeWidth, pipeHeight):
    pipeSouthImageName = Utils.resizeImage(Constants.BASE_PATH,
                                       Constants.PIPE_SOUTH_NAME,
                                       pipeWidth,
                                       pipeHeight)
    pipeSouth = pygame.image.load(pipeSouthImageName)
    return pipeSouth


from GameObject import GameObject
from GeneticClient import GeneticClient
import Constants
from Network import Network
import numpy as np
import pickle
import pygame

class Bird(GameObject, GeneticClient):
    def __init__(self, xCoordinate, yCoordinate, objectWidth, objectHeight, imageBasePath, imageName):

        self.imageBasePath = imageBasePath
        self.imageName = imageName

        # initialize features to some value
        self.yDistanceNorthPipe = 50
        self.yDistanceSouthPipe = Constants.GAP_BETWEEN_PIPES - self.yDistanceNorthPipe
        self.xDistancePipe = 100

        self.isJump = False
        self.jump = Constants.JUMP_DISTANCE
        self.score = 0
        self.health = Constants.GENETIC_LIFE
        self.alive = True
        self.lastPipeCrossed = None

        inputSize = 3
        hiddenLayersSize = [10, 5]
        outputSize = 2

        self.network = Network(inputSize, hiddenLayersSize, outputSize)

        super().__init__(xCoordinate, yCoordinate, objectWidth, objectHeight, imageBasePath, imageName)

    def copy(self):
        return Bird(self.xCoordinate, self.yCoordinate, self.objectWidth, self.objectHeight, self.imageBasePath, self.imageName )

    def recalculateFeatures(self, pipes):
        nearestPipeXDistance = 1000000
        nearestPipePair = None
        for pipePair in pipes:

            northPipe = pipePair[0]

            # pipe has already passed the bird but it is in frame
            if (northPipe.xCoordinate + Constants.PIPE_WIDTH) < self.xCoordinate:
                continue
            
            # bird is in between the north pipe and south pipe
            if (self.xCoordinate + Constants.BIRD_WIDTH) >= northPipe.xCoordinate & self.xCoordinate <= ( northPipe.xCoordinate + Constants.PIPE_WIDTH ):
                nearestPipeXDistance = 0
                nearestPipePair = pipePair
                break

            # update nearest pipe xDistance
            pipeDistance = northPipe.xCoordinate - self.xCoordinate
            if pipeDistance < nearestPipeXDistance:
                nearestPipePair = pipePair
                nearestPipeXDistance = pipeDistance

        self.xDistancePipe = nearestPipeXDistance
        self.yDistanceNorthPipe = nearestPipePair[0].yCoordinate + nearestPipePair[0].objectHeight - self.yCoordinate
        self.yDistanceSouthPipe = nearestPipePair[1].yCoordinate - self.yCoordinate

    def networkForwardStep(self):
        inputFeatures = np.array([self.yDistanceNorthPipe, self.yDistanceSouthPipe, self.xDistancePipe])
        return self.network.forwardStep(inputFeatures)

    def changeCoordinate(self, changeBy):
        self.yCoordinate += changeBy

    def getFitness(self):
        return self.health

    def getNetwork(self):
        return self.network

    def saveObject(self, pickleFilePath):
        with open(pickleFilePath, 'wb') as f:
            pickle.dump(self, f)

    def display(self, window):
        displayYCoordinate = self.yCoordinate
        displayXCoordinate = self.xCoordinate
        if displayYCoordinate > Constants.BIRD_Y_COORDINATE_MAX:
            displayYCoordinate = Constants.BIRD_Y_COORDINATE_MAX

        if displayYCoordinate < Constants.BIRD_Y_COORDINATE_MIN:
            displayYCoordinate = Constants.BIRD_Y_COORDINATE_MIN

        coordinates = (displayXCoordinate, displayYCoordinate)
        loadedImage = pygame.image.load(self.imagePath)
        window.blit( loadedImage, coordinates)


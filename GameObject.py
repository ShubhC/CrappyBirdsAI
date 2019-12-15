import os
import Utils
from enum import Enum
from PIL import Image
import Constants
from Network import Network
import numpy as np
import pygame

class GameObject(object):
    def __init__(self, xCoordinate, yCoordinate, objectWidth, objectHeight, imageBasePath, imageName):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        resizedImagePath = Constants.RESIZED_IMAGE_DIRECTORY 
        self.imagePath = Utils.generateResizedImage(imageBasePath, 
                                                    imageName,
                                                    resizedImagePath,
                                                    objectWidth,
                                                    objectHeight)
        if objectWidth == -1 or objectHeight == -1:
           self.objectWidth = 38
           self.objectHeight = 30
        else:
           self.objectWidth = objectWidth
           self.objectHeight = objectHeight

        self.hitbox = (xCoordinate, 
                       yCoordinate, 
                       xCoordinate + self.objectWidth, 
                       yCoordinate + self.objectHeight)

    def delImage(self):
        self.removeImg(self.imagePath)

    def removeImg(self, image_path):
        os.remove(image_path)
        # check if file exists or not
        if os.path.exists(image_path) is False:
            return True

    def display(self, window):
        loadedImage = pygame.image.load(self.imagePath)
        coordinates = (self.xCoordinate,self.yCoordinate)
        window.blit( loadedImage, coordinates)

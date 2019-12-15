# Utils functions
import Constants
from skimage import data, color
from resizeimage import resizeimage
from skimage.transform import rescale, resize, downscale_local_mean
from PIL import Image
import numpy as np
import cv2
import uuid
import os
import os.path
import numpy
import numpy as np

def getFileExtension(filename):
    return os.path.splitext(filename)[1]

def getUuid():
    return str(uuid.uuid4())

# Generate a resized image and returns its path
def generateResizedImage(basePath, imageName, resizedImagePath, newWidth = -1, newHeight = -1):
    if newWidth == -1 & newHeight == -1:
        return basePath + imageName
    if imageName == Constants.PIPE_NORTH_NAME:
        croppedImg = Image.open(basePath + imageName)
        croppedImg = croppedImg.crop((0,Constants.GROUND_Y_COORDINATE-newHeight,newWidth,Constants.GROUND_Y_COORDINATE))
        croppedImgName = basePath + Constants.RESIZED_IMAGE_DIRECTORY + getUuid() + getFileExtension(imageName);
        croppedImg.save(croppedImgName)
        croppedImg.close()
        return croppedImgName

    if imageName == Constants.PIPE_SOUTH_NAME:
        croppedImg = Image.open(basePath + imageName) 
        croppedImg = croppedImg.crop((0,0,newWidth,newHeight))
        croppedImgName = basePath + Constants.RESIZED_IMAGE_DIRECTORY + getUuid() + getFileExtension(imageName);
        croppedImg.save(croppedImgName)
        croppedImg.close()
        return croppedImgName
    
    resizedImageName = resizeImage(basePath,
                                   imageName,
                                   resizedImagePath,
                                   getUuid(),
                                   newWidth,
                                   newHeight)
    return resizedImageName

def image_resize(basePath, imageName, resizedImagePath, resizedImageName, width, height, inter = cv2.INTER_AREA):
    
    imagePath = basePath + imageName;
    image = load_image(imagePath)

    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # resize the image
    resized = cv2.resize(image, (width, height))

    resizedImagePath = basePath + resizedImagePath + resizedImageName + getFileExtension(imageName)
    save_image(resized, resizedImagePath)
    return resizedImagePath

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="uint8" )
    img.close()
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( npdata )
    img.save( outfilename )

def resizeImage(basePath, imageName, resizedImagePath, resizedImageName, dimX, dimY):
    return image_resize(basePath, imageName, resizedImagePath, resizedImageName, dimX, dimY)

def isCollision(birdObject, northPipeObject, southPipeObject, roofYCoordinate, birdMaxYCoordinate):
    return isCollisionBetweenGameObjects(birdObject, northPipeObject) or \
           isCollisionBetweenGameObjects(birdObject, southPipeObject) or \
           isCollisionBetweenBirdAndRoof(birdObject, roofYCoordinate) or \
           isCollisionBetweenBirdAndGround(birdObject, birdMaxYCoordinate)

def isCollisionBetweenGameObjects(gameObject1, gameObject2):    
    #### two object do not collide if one is entirely to left, right, top or bottom ###
    entireToLeft = (gameObject2.xCoordinate + gameObject2.objectWidth) < gameObject1.xCoordinate

    entireToRight = gameObject2.xCoordinate > (gameObject1.xCoordinate+gameObject1.objectWidth)

    entireToTop = (gameObject2.yCoordinate + gameObject2.objectHeight) < gameObject1.yCoordinate

    entireToBottom = gameObject2.yCoordinate > (gameObject1.yCoordinate + gameObject1.objectHeight)

    isCollision = not( entireToLeft or entireToRight or entireToTop or entireToBottom)

    return isCollision

def isCollisionBetweenBirdAndRoof(birdObject, roofYCoordinate):
    isCollision = not (birdObject.yCoordinate > roofYCoordinate)
    return isCollision

def isCollisionBetweenBirdAndGround(birdObject, groundYCoordinate):
    isCollision = not (birdObject.yCoordinate < groundYCoordinate)
    return isCollision

def removeElementsAtIndices(elements, indices):
    for index in sorted(indices, reverse=True):
        del elements[index]
    return elements

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def relu(Z):
    return np.maximum(0,Z)

def softmax(z):
    e_x = np.exp(z - np.max(z))
    return e_x / e_x.sum()

def removeElements(elements, indicesToRemove):
    indicesToRemove = set(indicesToRemove)
    elementsToKeep = list()
    for i in range(0,len(elements)):
        if i in indicesToRemove:
            continue
        elementsToKeep.append(elements[i])
    return elementsToKeep

import numpy as np
import Utils
import Constants
import random

class Layer(object):
    def __init__(self, inputSize, outputSize, activationFunction):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.w = None
        self.b = None
        self.activationFunction = activationFunction

    def runTransformation(self, input):
        # transpose(W).X + b
        linearTransformation = np.dot(np.transpose(self.w), input) + self.b
        if self.activationFunction == Constants.RELU_ACTIVATION_FUNCTION:
            return Utils.relu(linearTransformation)
        elif self.activationFunction == Constants.IDENTITY_ACTIVATION_FUNCTION:
            return linearTransformation
        elif self.activationFunction == Constants.SIGMOID_ACTIVATION_FUNCTION:
            return Utils.sigmoid(linearTransformation)
        elif self.activationFunction == Constants.SOFTMAX_ACTIVATION_FUNCTION:
            return Utils.softmax(linearTransformation)
        else:
            raise Exception("Activation function not supported")

    def copyLayer(self):
        newLayer = Layer(self.inputSize, self.outputSize, self.activationFunction)
        newLayer.w = np.copy(self.w)
        newLayer.b = np.copy(self.b)
        return newLayer

    def crossover(self, otherLayer, crossoverRate):
        parentA = self.copyLayer()
        parentB = otherLayer.copyLayer()
        
        offspring = parentA

        # crossover w    
        lenW = parentA.w.shape[0] * parentA.w.shape[1]
        eleToCrossover = int( lenW * crossoverRate )

        newArr = np.concatenate( (np.ones(eleToCrossover), np.zeros(lenW-eleToCrossover)) )
        np.random.shuffle(newArr)
        newArr = np.reshape(newArr, parentA.w.shape)

        offspring.w = np.multiply(parentA.w, newArr) + np.multiply(parentB.w,  np.where(newArr == 0,1,0))

        # crossover b
        lenB = len(parentA.b)
        eleToCrossover = int( lenB * crossoverRate )
        
        newArr = np.concatenate( (np.ones(eleToCrossover), np.zeros(lenB-eleToCrossover)) )
        np.random.shuffle(newArr)
        newArr = np.reshape(newArr, parentA.b.shape)

        offspring.b = np.multiply(parentA.b, newArr) + np.multiply(parentB.b, np.where(newArr == 0,1,0))

        return offspring

    def mutate(self, mutationRate, mutationStrength):
        # mutate b
        lenB = len(self.b)
        eleToMutate = int( lenB * mutationRate )
       
        bMutations = np.concatenate( (np.random.normal(size=eleToMutate)*mutationStrength, np.zeros(lenB-eleToMutate)) )
        np.random.shuffle(bMutations)
        bMutations = np.reshape(bMutations, self.b.shape)

        self.b = self.b + bMutations

        # mutate w
        lenW = self.w.shape[0] * self.w.shape[1]
        eleToMutate = int( lenW * mutationRate )
        
        wMutations = np.concatenate( (np.random.normal(size=eleToMutate)*mutationStrength, np.zeros(lenW-eleToMutate)) )
        np.random.shuffle(wMutations)
        wMutations = np.reshape(wMutations, self.w.shape)

        self.w = self.w + wMutations

        return self


class InputLayer(Layer):
    def __init__(self, inputSize, outputSize, activationFunction=Constants.IDENTITY_ACTIVATION_FUNCTION):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.activationFunction = activationFunction
        self.w = np.ones((inputSize,1))
        self.b = np.zeros(inputSize)

    def runTransformation(self, input):
        return super().runTransformation(input)

class HiddenLayer(Layer):
    def __init__(self, inputSize, outputSize, activationFunction=Constants.RELU_ACTIVATION_FUNCTION):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.activationFunction = activationFunction
        self.w = np.random.rand(inputSize, outputSize)
        self.b = np.random.rand(outputSize)

    def runTransformation(self, input):
        return super().runTransformation(input)

class OutputLayer(Layer):
    def __init__(self, inputSize, outputSize, activationFunction=Constants.SOFTMAX_ACTIVATION_FUNCTION):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.activationFunction = activationFunction
        self.w = np.random.rand(inputSize, outputSize)
        self.b = np.random.rand(outputSize)

    def runTransformation(self, input):
        return super().runTransformation(input)
 
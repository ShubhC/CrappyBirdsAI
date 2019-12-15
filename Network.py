import numpy as np
from Layer import Layer, InputLayer, HiddenLayer, OutputLayer

# a simple neural network
# there is no notion of gradients/backpropagation here
# the model learns the parameters by genetic algorithms
class Network(object):
    def __init__(self, inputSize, hiddenLayersSize, outputSize):
        self.inputSize = inputSize
        self.hiddenLayersSize = hiddenLayersSize
        self.outputSize = outputSize

        self.inputLayer = InputLayer(self.inputSize, hiddenLayersSize[0])

        previousLayerSize = self.inputSize
        self.hiddenLayers = list()
        for i in range(0, len(self.hiddenLayersSize)):
            hiddenLayerSize = hiddenLayersSize[i]
            hiddenLayer = HiddenLayer(previousLayerSize, hiddenLayerSize)
            self.hiddenLayers.append( hiddenLayer )
            previousLayerSize = hiddenLayerSize
        
        self.outputLayer = OutputLayer(self.hiddenLayersSize[-1], self.outputSize)

    def forwardStep(self, input):
        inputLayerOutput = self.inputLayer.runTransformation(input)
        
        previousLayerOutput = inputLayerOutput
        for i in range(0, len(self.hiddenLayers)):
            hiddenLayer = self.hiddenLayers[i]
            hiddenLayerOutput = hiddenLayer.runTransformation(previousLayerOutput)
            previousLayerOutput = hiddenLayerOutput
        
        outputLayerOutput = self.outputLayer.runTransformation(previousLayerOutput)
        return outputLayerOutput
    
    def copy(self):
        newNetwork = Network(self.inputSize, self.hiddenLayersSize, self.outputSize)
        return newNetwork

    def crossover(self, otherNetwork, crossoverRate):
        offspring = self.copy()
        offspring.inputLayer = self.inputLayer.crossover(otherNetwork.inputLayer, crossoverRate)
        offspring.hiddenLayers = [self.hiddenLayers[i].crossover(otherNetwork.hiddenLayers[i], crossoverRate)  for i in range(0,len(self.hiddenLayers))]
        offspring.outputLayer = self.outputLayer.crossover(otherNetwork.outputLayer, crossoverRate)
        return offspring

    def mutate(self, mutationRate, mutationStrength):
        self.inputLayer.mutate(mutationRate, mutationStrength)
        [self.hiddenLayers[i].mutate(mutationRate, mutationStrength) for i in range(0, len(self.hiddenLayers))]
        self.outputLayer.mutate(mutationRate, mutationStrength)



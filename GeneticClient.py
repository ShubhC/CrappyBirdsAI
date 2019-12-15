import abc

class GeneticClient(abc.ABC):
    @abc.abstractmethod
    def getFitness(self):
        pass

    @abc.abstractmethod
    def getNetwork(self):
        pass
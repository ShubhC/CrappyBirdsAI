import random
import Utils
from Network import Network
from GeneticClient import GeneticClient
import numpy as np
from Bird import Bird
import Constants
import math

class GeneticAlgorithm(object):
    def __init__(self, population, nSelections, crossoverRate, mutationRate, mutationStrength):
        # population of birds
        self.population = population

        # number of selections
        self.nSelections = nSelections

        # gene interchange rate
        self.crossoverRate = crossoverRate
        
        self.mutationRate = mutationRate
        self.mutationStrength = mutationStrength

        self.iterationNumber = 0
        
    def evolve(self):
        
        self.iterationNumber += 1

        # 1. kill all ghosts
        alivePopulation = list()
        for geneticClient in self.population:
            if geneticClient.alive:
                alivePopulation.append(geneticClient)

        self.population = alivePopulation

        self.nSelections =  max(int( Constants.MAX_POPULATION_SIZE*0.2 - self.iterationNumber**2 ), 0)

        # 2. selection of parents 
        self.selections = self.selection(self.nSelections)

        # 3. crossover
        self.offsprings = self.crossover(self.population, self.selections, self.crossoverRate)

        # 4. add offsprings back to population
        self.population = self.population + self.offsprings if len(self.population) != 0 else self.offsprings

        # 5. add selections back to population
        self.population = self.population + self.selections if len(self.selections) != 0 else self.population

        # 6. mutations
        self.population = self.mutation(self.population, self.mutationRate, self.mutationStrength)

        return self.population

    def selection(self, nSelections):

        if( len(self.population) < nSelections ):
            selections = self.population
            self.population = list()
            return selections

        # sample parents based on fitness scores
        sumScores = sum( geneticClient.getFitness() for geneticClient in self.population)
        populationProb = None
        if sumScores == 0:
            populationProb = [1/len(self.population) for i in range(0, len(self.population))]
        else:
            populationProb = [ geneticClient.getFitness()/sumScores for geneticClient in self.population]
        if len(self.population) == 0:
            return self.population
        all_index = np.array([i for i in range(0,len(self.population))])
        selections_indices = set(np.random.choice(all_index, nSelections, p=populationProb))

        selections = list()
        selectionsRemovedPopulation = list()
        for i in range(0,len(self.population)):
            if i in selections_indices:
                selections.append(self.population[i])
            else:
                selectionsRemovedPopulation.append(self.population[i])
        self.population = selectionsRemovedPopulation

        return selections

    def crossover(self,population,selections,crossoverRate):
        if len(population) == 0:
            return population

        offsprings = list()

        for selection in selections:
            parentA = selection.copy()
            parentB = population[ int(random.randint(0, len(population)-1)) ].copy()  if len(population) > 1 else population[0].copy()
            parentA.network = parentA.getNetwork().crossover(parentB.getNetwork(), crossoverRate)
            min_health = min(parentA.health, parentB.health)
            max_health = max(parentA.health, parentB.health)
            parentA.health = random.randint(min_health, max_health) if min_health != max_health else min_health

            offsprings.append(parentA)

        return offsprings

    def mutation(self, population, mutationRate, mutationStrength):
        for offspring in population:
            offspring.getNetwork().mutate(mutationRate*max(0, (Constants.MAX_POPULATION_SIZE-self.iterationNumber**2)/Constants.MAX_POPULATION_SIZE), mutationStrength)
        return population
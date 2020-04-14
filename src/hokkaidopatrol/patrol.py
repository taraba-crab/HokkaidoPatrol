# -*- coding: utf-8 -*-

from typing import List
from random import shuffle, sample
from copy import deepcopy

from .genetic import Chromosome
from .genetic import GeneticAlgorithm
from .inputs import userinput
from .inputs import randominput
from .inputs import fileinput
from .cities import cities

distances = {}

class Patrol(Chromosome):
    def __init__(self, data: List[str]):
        self.data = data

    def fitness(self) -> float:
        total = 0
        for i in range(len(self.data)-1):
            u, v = self.data[i], self.data[i+1]
            total += distances[u][v]
        
        total += distances[self.data[0]][self.data[-1]]

        return -total

    @classmethod
    def random_instance(cls, cities: List[str]):
        cities_ = deepcopy(cities)
        shuffle(cities_)
        return Patrol(cities_)

    def crossover(self, other):
        # PMXによる交叉
        child1 = deepcopy(self)
        child2 = deepcopy(other)
        
        l, r = sample(range(len(self.data)), k=2)
        if r < l:
            l, r = r, l

        changing1 = set()
        changing2 = set()
        for i in range(l, r):
            child1_e, child2_e = child1.data[i], child2.data[i]
            child1.data[i], child2.data[i] = child2_e, child1_e
            changing1.add(child2_e)
            changing2.add(child1_e)

        conflict1: List[int] = []
        conflict2: List[int] = []
        for i in range(l):
            if child1.data[i] in changing1:
                conflict1.append(i)

            if child2.data[i] in changing2:
                conflict2.append(i)

        for i in range(r, len(self.data)):
            if child1.data[i] in changing1:
                conflict1.append(i)

            if child2.data[i] in changing2:
                conflict2.append(i)

        for i, j in zip(conflict1, conflict2):
            child1.data[i], child2.data[j] = child2.data[j], child1.data[i]

        return child1, child2

    def mutate(self):
        x, y = sample(range(len(self.data)), k=2)
        self.data[x], self.data[y] = self.data[y], self.data[x]

    def __str__(self):
        return "->".join(self.data) + f": {self.fitness()} km"


def main():
    global distances
    # ファイルからの入力
    initial, distances = fileinput.file_input()

    # CLIからの入力
    #initial, distances = userinput.user_input()

    # ランダム入力
    # initial, distances = randominput.random_select(10)

    print(initial)
    print(distances)

    initial_population = [Patrol.random_instance(initial) for _ in range(50)]

    ga = GeneticAlgorithm(initial_population=initial_population,
                          threshold=0,
                          max_generations=5000,
                          mutation_chance=0.2,
                          crossover_chance=0.7,
                          selection_type=GeneticAlgorithm.SelectionType.TOURNAMENT
                          )
    result = ga.run()
    print(result)

if __name__ == "__main__":
    main()

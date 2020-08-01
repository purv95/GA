import random
import timeit
import numpy as np
import csv

Number_Of_Generations = 100
seed = 1
Pop_Size = 20  
Total_Weight_Bag  = 0
Total_Size_Items_Bag  = 0
items = {}
Tournament_size = int(Pop_Size/4)
Maximum_Weight  = random.randint(10000, 20000)
Maximum_Size = random.randint(10000, 20000) 
Number_Of_Items  = random.randint(100, 200)
Mutate_Prob  = 0.3  
Crossover_Prob = 0.9

generate = True


def read():
    with open('Book1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if(i > 0):
                items[i-1] = row
                i += 1
            else:
                Number_Of_Items  = row[0]
                Maximum_Weight  = row[1]
                Maximum_Size = row[2]
                i += 1

    for row in range(len(items)):
        for col in range(len(items[row])):
            items[row][col] = int(items[row][col])
        print(items[row])


def initialize_knapsack_table():
    
    random_max_weight = 0
    random_max_size = 0
    random_max_cost = 0
    print("-------| Random Available Items |------- ")
    print("Num       W   C   S")

    for i in range(Number_Of_Items ):
        weight_artifact = random.randint(
            1, int(Maximum_Weight /Number_Of_Items /10))  
        cost_artifact = random.randint(1, Number_Of_Items ) 
        size_artifact = random.randint(
            1, int(Maximum_Size/Number_Of_Items /10))
        # Store in Items variable
        items[i] = weight_artifact, cost_artifact, size_artifact
        print("Item {} : {}".format((i + 1), items[i])) 
        random_max_size += size_artifact 
        random_max_weight += weight_artifact
        random_max_cost += cost_artifact
    print("Total Size: {}  Total Cost:{} Total Weight: {} ".format(
        random_max_size, random_max_cost, random_max_weight))

    ls = [Number_Of_Items , Maximum_Weight , Maximum_Size]
    with open("Book1.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(ls)
    for i in range(Number_Of_Items ):
        with open("Book1.csv", 'a+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(items[i])


def print_knapsack_table():
    
    print("\n\n-------| Total Available Items |------- ")
    print("Num  weight  cost  size")
    for i in range(Number_Of_Items ):
        print(chr(i + 65), end='     ')
        print(items[i][0], end='     ')
        print(items[i][1], end='     ')
        print(items[i][2])


class Individual:
    def __init__(self):
        # Initializes the genome and fitness
        self.gene = []
        self.fitness = 0

    def generate(self):
        for i in range(Number_Of_Items ):
            self.gene.append(random.randint(0, 1))
        self.fitness = self.fitness_function()

    def fitness_function(self):
        """ fitness function is total value of the items in the knapsack
            If the weight exceeds the maximum weight - fitness becomes 0"""
        fitness = 0
        weight = 0
        size_arti = 0
        for i in range(Number_Of_Items ):
            if self.gene[i] == 1:
                weight += items[i][0]
                fitness += items[i][1]
                size_arti += items[i][2]
        if (weight > Maximum_Weight  and size_arti < Maximum_Size) or (weight < Maximum_Weight  and size_arti > Maximum_Size):
            fitness = int(fitness / 2)
        elif weight < Maximum_Weight  and size_arti < Maximum_Size:
            fitness = fitness
        elif weight > Maximum_Weight  or size_arti > Maximum_Size:
            fitness = 0
        return fitness

    def mutate(self):
        """ Chooses a random item and topples its presence """
        for i in range(seed):
            mutate_index = random.randint(0, Number_Of_Items  - 1)
            self.gene[mutate_index] = bool(self.gene[mutate_index]) ^ 1
            self.fitness = self.fitness_function()


class Selection:
    def __init__(self, llist):
        self.populationlist = llist

    def tournament(self):
        tour_pop = []
        for i in range(Tournament_size):
            chromo = random.randint(0, Pop_Size - 1)
            tour_pop.append(chromo)

        maximum = 0
        for i in tour_pop:
            if self.populationlist[i].fitness > maximum:
                maximum = i

        return maximum


class Population:
    def __init__(self):
        self.populationlist = []

    def generate_random_population(self):
        """ Generates a random list of population """
        for i in range(Pop_Size):
            chromosome = Individual()
            chromosome.generate()
            self.populationlist.append(chromosome)

    def sort_and_cut_growth(self):
        """ The population list is sorted according to the fitness function and the least fit ones are
            removed to maintain the population size """

        self.populationlist = sorted(
            self.populationlist, key=lambda x: x.fitness, reverse=True)
        self.populationlist = self.populationlist[:Pop_Size]

    def crossover(self):
        crossover1 = Selection(self.populationlist).tournament()
        crossover2 = Selection(self.populationlist).tournament()
        spiltpoint = random.randint(0, Number_Of_Items  - 1)
        child1 = Individual()
        child2 = Individual()
        list1 = []
        list2 = []
        child1.gene = self.populationlist[crossover1].gene
        child2.gene = self.populationlist[crossover2].gene
        list1 = child1.gene[:spiltpoint] + child2.gene[spiltpoint:]
        list2 = child2.gene[:spiltpoint] + child1.gene[spiltpoint:]
        child1.gene = list1
        child2.gene = list2
        child1.fitness = child1.fitness_function()
        child2.fitness = child2.fitness_function()
        return child1, child2
import random
import timeit
import numpy as np
import csv
import matplotlib.pyplot as plt
from GA import *


def Draw_Mutation():
    Mutate_Prob  = 0.3
    llist1 = []
    llist2 = []
    for i in range(3):
        Mutate_Prob  += 0.3
        read()
        knapsack = Population()
        # For first generation it is randomly populated
        knapsack.generate_random_population()
        condition = True
        z = 0
        maxfit = []
        meanfit = []

        while condition:
            Total_Weight_Bag  = 0
            Total_Size_Items_Bag  = 0

            fit = 0
            for i in range(Pop_Size):
                fit += knapsack.populationlist[i].fitness
            meanfit.append(fit/Pop_Size)

            size = int(Pop_Size / 2 + 1)
            for y in range(size):  # Performs crossover
                offspring1, offspring2 = knapsack.crossover()
                if random.random() > Mutate_Prob :  # if greater than given probability mutation occurs
                    offspring1.mutate()
                if random.random() > Mutate_Prob :
                    offspring2.mutate()
                # After mutation it is appended to the list
                knapsack.populationlist.append(offspring1)
                knapsack.populationlist.append(offspring2)
            z += 1
            knapsack.sort_and_cut_growth()  # At the end of generation death cycle occurs

            meanfit.append(fit/Pop_Size)
            size = int(Pop_Size * Crossover_Prob)

            for i in range(Number_Of_Items ):  # Prints the solution set
                if knapsack.populationlist[0].gene[i] == 1:
                    Total_Weight_Bag  = Total_Weight_Bag  + items[i][0]
                    Total_Size_Items_Bag  = Total_Size_Items_Bag  + \
                        items[i][2]

            rangerW = range(Maximum_Weight  - 5, Maximum_Weight )
            rangerS = range(Maximum_Size - 10, Maximum_Size)

            if (Total_Weight_Bag  in rangerW) and (Total_Size_Items_Bag  in rangerS):
                condition = False
            elif z > Number_Of_Generations:
                condition = False
            elif Total_Weight_Bag  > Maximum_Weight  or Total_Size_Items_Bag  > Maximum_Size:
                condition = False
            else:
                condition = True
            maxfit.append(knapsack.populationlist[0].fitness)
        llist1.append(meanfit)
        llist2.append(maxfit)

    plt.xlabel("Generation")
    plt.ylabel("Fitness ")

    mut = 0.3
    for i in range(3):
        llist5 = []
        for j in range(len(llist2[i])):
            llist5.append(j)
        plt.plot(llist5, llist2[i], label='Mutation rate:'+str(mut))
        mut += 0.3
    plt.legend()
    plt.show()


Draw_Mutation()
from GA import *

if __name__ == "__main__":
    tic = timeit.default_timer()

    if(generate):
        read()
    else:
        initialize_knapsack_table() 
    knapsack = Population()
    # For first generation it is randomly populated
    knapsack.generate_random_population()
    condition = True
    z = 0
    while condition:
        Total_Weight_Bag  = 0
        Total_Size_Items_Bag  = 0
        print("\nGeneration: {}".format((z + 1)))
        for i in range(Pop_Size):
            print("Genome: {}  Fitness : {}  ".format(knapsack.populationlist[i].gene,
                                                      knapsack.populationlist[i].fitness))
        size = int(Pop_Size * Crossover_Prob)
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
        print("z: {} , Iteration : {}".format(z, Number_Of_Generations))
        knapsack.sort_and_cut_growth()  # cycle finishes at end
        for i in range(Number_Of_Items ):  # solution set
            if knapsack.populationlist[0].gene[i] == 1:
                Total_Weight_Bag  = Total_Weight_Bag  + items[i][0]
                Total_Size_Items_Bag  = Total_Size_Items_Bag  + \
                    items[i][2]
        print("weight: {} , size : {}".format(
            Total_Weight_Bag , Total_Size_Items_Bag ))

        rangerW = range(Maximum_Weight  - 5, Maximum_Weight )
        rangerS = range(Maximum_Size - 10, Maximum_Size)

        print("rangerW: {} , rangerS : {}".format(
            Total_Weight_Bag  in rangerW, Total_Size_Items_Bag  in rangerS))

        if (Total_Weight_Bag  in rangerW) and (Total_Size_Items_Bag  in rangerS):
            condition = False
            print("calling False")
        elif z > Number_Of_Generations:
            condition = False
        elif Total_Weight_Bag  > Maximum_Weight  or Total_Size_Items_Bag  > Maximum_Size:
            condition = False
        else:
            condition = True
            print("calling True")

    print_knapsack_table()

    print("\nBest Individual: {}".format(knapsack.populationlist[0].gene))
    Total_Weight_Bag  = 0
    Total_Size_Items_Bag  = 0
    print("Items kept in the bag are: ", end='')
    for i in range(Number_Of_Items ):  # solution set
        if knapsack.populationlist[0].gene[i] == 1:
            Total_Weight_Bag  = Total_Weight_Bag  + items[i][0]
            Total_Size_Items_Bag  = Total_Size_Items_Bag  + \
                items[i][2]
            print(chr(i + 65), end=' ')

    print("\nTotal Cost of Items in Bag: {}".format(
        knapsack.populationlist[0].fitness))
    print("Total weight of Items in Bag: {}".format(Total_Weight_Bag ))
    print("Total size of Items in Bag: {}".format(Total_Size_Items_Bag ))
    toc = timeit.default_timer()
    timetaken = (toc - tic)
    print("Time taken : ", float("{0:.2f}".format(timetaken)))
    

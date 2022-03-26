import math, random, re
from pandas import DataFrame

# Sets up global variables
global CityList, CitiesOrder, PopSize, Population, Fittness, NewPopulation
global bestOrder, bestDistance, maxGens, RateOfMutation, CrossOverProb
CityList = []
CitiesOrder = []
PopSize = 0
Population = []
Fittness = []
NewPopulation = []
bestOrder = None
bestDistance = math.inf
maxGens = 0
RateOfMutation = -1
CrossOverProb = -1

def main():
    global CityList, CitiesOrder, PopSize, Population, Fittness, NewPopulation
    global bestOrder, bestDistance, maxGens, RateOfMutation, CrossOverProb
    
    # try statement reads the file for x, y cords. and the order to traverse the city in
    try:
        readFile = open('D:\\COSC 3P71\\Term Project\\Assignment 2\\Ulysses22.txt', 'r') # file path, change if needed

        for i in range(9):
            charIndex = readFile.read(1) # reads it as 2 characters instead of 1 because 2 digit numbers
            
            if charIndex == '': # Might not need this line since for loop is used instead of while loop
                break
            
            CitiesOrder.append(int(charIndex) - 1) # - 1 for indexing in 0 based list

            coordinates = readFile.readline()

            coordinates =  coordinates.strip()
            coordinates = coordinates.strip(' \t\n\r')
            re.sub('[\s+]', '', coordinates)

            corX = coordinates[:5]
            corY = coordinates[-5:]

            CityList.append((float(corX), float(corY)))
        
        while True:
            charIndex = readFile.read(2) # reads it as 2 characters instead of 1 because 2 digit numbers
            
            if charIndex == '': # Might not need this line since for loop is used instead of while loop
                break
            
            CitiesOrder.append(int(charIndex) - 1) # - 1 for indexing in 0 based list

            coordinates = readFile.readline()

            coordinates =  coordinates.strip()
            coordinates = coordinates.strip(' \t\n\r')
            re.sub('[\s+]', '', coordinates)

            corX = coordinates[:5]
            corY = coordinates[-5:]

            CityList.append((float(corX), float(corY)))

    # except statements catch the possible errors that could pop up
    except FileNotFoundError as err:
        print(f'File not found. {err}')
    
    except ValueError as err:
        print(f'Invalid input in file, expect only int. {err}')

    print(f'\n{CityList}\n')

    # option to read the parameters for the algorithm from a file    
    readparaFile = None

    while True:
        readparaFile = input('Read parameters from file? (y/n): ')

        if readparaFile == 'y' or  readparaFile == 'n':
            break

    # if manual selection is selected this runs
    if readparaFile == 'n':
        
        # setting random seed again while the program is running does not work (or atleast i couldn't figure out the way to do it)
        randomNumSeed = None

        while randomNumSeed == None:
            try: # sets up the seed for the ranomd number generator
                randomNumSeed = int(input('Enter a seed for the random number generator: '))
            
            except ValueError as err:
                print(f'Invalid input. {err}')
        
        random.seed(randomNumSeed)

        PopSize = None

        # creates the population size
        while PopSize == None:
            try:
                PopSize = int(input('Enter a population size: '))
                
            except ValueError as err:
                print(f'Invalid input. {err}')

        # sets the max number of generations the GA will run for
        maxGens = None

        while maxGens == None:
            try:
                maxGens = int(input('Enter the number of generations to have: '))
            
            except ValueError as err:
                print(f'Invalid input. {err}')
        
        # sets the k value to be used by the tournement selection
        k = -1

        while k < 2 or k > 5:
            try:
                k = int(input('Enter value of k (between 2 and 5): '))
            
            except ValueError as err:
                print(f'Invalid input. {err}')

        # selects how the algorithm will 'reproduce' from either Uniform Order Crossover or Two Point Crossover
        CrossOption = -1

        while CrossOption < 1 or CrossOption > 2:
            try:
                CrossOption = int(input('Enter 1 to use UniformCrossover, or 2 to use two point crossover: '))

            except ValueError as err:
                print(f'Invalid input. {err}')
        
        # sets the % chance to reproduce as a value between 0 and 1
        CrossOverProb = -1

        while CrossOverProb > 1 or CrossOverProb < 0:
            try:
                CrossOverProb = float(input('Enter rate of crossover as a number between 0 and 1: '))
            
            except ValueError as err:
                print(f'Invalid input. {err}')

        # sets the % chance to mutate as a value between 0 and 1
        RateOfMutation = -1

        while RateOfMutation > 1 or RateOfMutation < 0:
            try:
                RateOfMutation = float(input('Enter rate of mutation as a number between 0 and 1: '))
            
            except ValueError as err:
                print(f'Invalid input. {err}')
    
    elif readparaFile == 'y':
        paraFile = open('D:\\COSC 3P71\\Term Project\\Assignment 2\\para.txt', 'r') # file path, change if needed
        
        randomNumSeed = int(paraFile.readline())
        PopSize = int(paraFile.readline())
        maxGens = int(paraFile.readline())
        k = int(paraFile.readline())
        CrossOption = int(paraFile.readline())
        CrossOverProb = int(paraFile.readline())
        RateOfMutation = int(paraFile.readline())

    # this sets up the initial population as a random shuffle of the City order to traverse through
    while len(Population) < PopSize:
        temp = CitiesOrder.copy()

        random.shuffle(temp) # generates the initial random population of the order to traverse in

        if temp not in Population: # only adds the new order created above if it doesn't already exist in the population/chromosome
            Population.append(temp)
    
    # ------------------------- MAIN Function/loop that does everything ----------------------------
    bestFit = [] # best fittness values are stored in here to print to an excell file
    avgFit = [] # average fittness values are stored in here to print to an excell file
    
    for i in range(maxGens):
        calculateFittness() # calculates the fittness value of all the orders in the population
        
        bestFittness, averageFittness = findBestFittness() # finds the best and average fittness values
        bestFit.append(bestFittness) # appends the best fittness value to the list
        avgFit.append(averageFittness) # appends the average fittness value to the list
        
        print(f"Best fittness of Generation {i} is {bestFittness} and average of fittness of this generation is {averageFittness}. Popsize: {len(Population)}") # prints relevent information to the console
        
        makeNextGen(RateOfMutation, CrossOverProb, CrossOption, k) # creats the next generation from the current population

    df = DataFrame({'Best of the Gen': bestFit, 'Average of Gen': avgFit}) # creates an excel file with the best fittness and the average fittness of each generation

    df.to_excel('D:\\COSC 3P71\\Term Project\\Assignment 2\\test.xlsx', sheet_name='sheet1', index=False) # saves the excel file
    
    print(f'\nBest route: {bestOrder} with distance: {round(bestDistance, 2)}.') # prints out the best route found while running the G.A.

# creates the next generation of the orders
def makeNextGen(MutationRate, CrossOverProbability, crossOverOption, k):
    global Population, NewPopulation, Fittness, CityList
    NewPopulation = [] # blanks the new population of remaining values

    if crossOverOption == 1: # runs the uniform order crossover algorithm
        bestofgen = findBestOfGen(Population) # gets the elite of this generation and moves it to the new population
        
        NewPopulation.append(bestofgen.copy())
        
        while len(NewPopulation) <= PopSize - 1: # populates the new population based on the last generation, - 1 because there is one elite being moved into 
            
            # This method will select 2 parents and subject them to a tournement and select them to be crossovered
            parent1 = tournamentSelection(Population, k)
            parent2 = tournamentSelection(Population, k)

            # creates children of the parents using uniform order crossover
            childOrder1, childOrder2 = UniformOrderCrossOver(parent1, parent2, CrossOverProbability)

            # mutates the children if the mutation rate allows
            mutateOrder(childOrder1, MutationRate)
            mutateOrder(childOrder2, MutationRate)
            
            # adds the first child into the new population
            NewPopulation.append(childOrder1.copy())
            
            if len(NewPopulation) < PopSize: # only adds the second child if the list has not reached max size
                NewPopulation.append(childOrder2.copy())
    
    else: # runs the two point crossover algorithm
        bestofgen = findBestOfGen(Population) # gets the elite of this generation and moves it to the new population
        
        NewPopulation.append(bestofgen.copy())

        while len(NewPopulation) <= PopSize - 1: # populates the new population based on the last generation, - 1 because there is one elite being moved into 
            # This method will select 2 parents and subject them to a tournement and select them to be crossovered
            parent1 = tournamentSelection(Population, k)
            parent2 = tournamentSelection(Population, k)

            # creates children of the parents using uniform order crossover
            childOrder1, childOrder2 = twoPointCrossOver(parent1, parent2, CrossOverProbability)

            # mutates the children if the mutation rate allows
            mutateOrder(childOrder1, MutationRate)
            mutateOrder(childOrder2, MutationRate)
            
            # adds the first child into the new population
            NewPopulation.append(childOrder1.copy())
            
            if len(NewPopulation) < PopSize: # only adds the second child if the list has not reached max size
                NewPopulation.append(childOrder2.copy())

    Population = [] # scraps the old generation and sets the new generation as the current population
    Population = NewPopulation.copy() # sets the population equal to the new population and work on it

def twoPointCrossOver(Parent1, Parent2, crossOverProb):
    Child1 = []
    Child2 = []
    rand = random.random() # check if crossover will take place

    if rand <= crossOverProb: # only performs a crossover if the random chance is <= the probability
        # gets a start and end point and from parent 1 from child 1
        start = random.randrange(0, len(Parent1))
        end = random.randrange(start, len(Parent1))
        Child1 = Parent1[start: end].copy()

        # gets a start and end point and from parent 2 from child 2
        start = random.randrange(0, len(Parent1))
        end = random.randrange(start, len(Parent1))
        Child2 = Parent2[start: end].copy()

        for i in Parent2: # child 1 gets missing material(what it didn't inheriate) from parent 2
            if i not in Child1:
                Child1.append(i)

        for i in Parent1: # child 2 gets missing material(what it didn't inheriate) from parent 1
            if i not in Child2:
                Child2.append(i)

        return Child1.copy(), Child2.copy()

    else: # else just returns the parents if random chance is less than needed
        return Parent1.copy(), Parent2.copy()

def UniformOrderCrossOver(Parent1, Parent2, crossOverProb):
    rand = random.random()

    if rand <= crossOverProb: # only performs a crossover if the random chance is <= the probability
        mask = []
        Child1, Child2 = [], []
        
        for i in range(len(Parent1)): # creates the mask to use
            mask.append(random.choice((0, 1)))
        
        for i in range(len(mask)): # if the mask allows, populates the child with information from the other parent
            if mask[i] == 1:
                getParent1 = Parent1[i]
                getParent2 = Parent2[i]

                Child2.append(getParent1)
                Child1.append(getParent2)

            else: # else sets the value as -1 to then be repaired below
                Child2.append(-1)
                Child1.append(-1)
        
        repairGenes(Child1, Child2, Parent1, Parent2) # repairs the genes of the children for what it didn't get from it's parents

        return Child1.copy(), Child2.copy() # returns the children

    else: # else just returns the parents
        return Parent1.copy(), Parent2.copy()

# repairs the children's genes with information from parents 
def repairGenes(Child1, Child2, Parent1, Parent2):
    counter = 0
    emptySlots = []

    # ------- Repairs child 1 genes -----------
    for i in range(len(Child1)):
        if Child1[i] == -1:
            emptySlots.append(i)
    
    counter = 0

    for i in Parent1:
        if i not in Child1:
            Child1[emptySlots[counter]] = i
            counter += 1

    counter = 0
    emptySlots = []

    # ------- Repairs child 2 genes -----------
    for i in range(len(Child2)):
        if Child2[i] == -1:
            emptySlots.append(i)
    
    counter = 0

    for i in Parent2:
        if i not in Child2:
            Child2[emptySlots[counter]] = i
            counter += 1

def tournamentSelection(Pop, k):
    global CityList
    arena = []
    bestFit = 0

    for i in range(k): # runs k amount of times
        arena.append(Pop[ random.randint(0, len(Pop) - 1) ].copy()) # copies a random order from the array to the arena

    for i in arena: # selects people from the arena and compares them against eachother
        dist = calculateDistance(CityList, i)
        fitt = 1 / dist
        
        if fitt > bestFit: # if the fittness of this one is better, sets it up as the order to return
            bestFit = fitt
            OrderToReturn = i.copy()

    return OrderToReturn.copy()

# mutates the children/order if the rate allows
def mutateOrder(Order, rate):
    for i in range(len(CityList)):
        rand = random.random()

        if rand <= rate:
            index1 = math.floor(random.randrange(0, len(Order) - 1))
            index2 = math.floor(random.randrange(0, len(Order) - 1))

            swapElements(Order, index1, index2) # mutation is a swap

# finds the best and average fittness of the order
def findBestFittness():
    global Fittness
    bestFittness = Fittness[0] #compareFittness # also assigns a best value discovered
    averageFittness = 0

    for i in Fittness:
        if i < bestFittness:
            bestFittness = i

        averageFittness += i

    averageFittness = averageFittness / len(Fittness)

    return bestFittness, averageFittness

def findBestOfGen(ArrayOrder): # finds the best order, the one with the lowest distance/best fittness of this generation
    global CityList, CitiesOrder

    # inits a random order as the best
    testOrder = ArrayOrder[random.randint(0, len(ArrayOrder) - 1)]
    best = calculateDistance(CityList, testOrder)
    bestOrderofGen = testOrder.copy()
    
    for i in ArrayOrder: # compares the other order against eachother and selects the best one
        currdist = calculateDistance(CityList, i)

        if currdist < best:
            best = currdist
            bestOrderofGen = i.copy()

    return bestOrderofGen.copy() # returns the best order found

def calculateFittness(): # original algorithm was to calculate how close the current orders to the last generations best distance and assign a fitness value based on that but this works better
    global bestDistance, Fittness, bestOrder, CityList
    Fittness = []

    # calculates the distance and divides it by 1 to represent it as a fittness value for the order
    for i in Population:
        distance = calculateDistance(CityList, i)
        Fittness.append(1 / distance)

        if distance < bestDistance:
            bestDistance = distance
            bestOrder = i.copy() # sets it as the best order 

# def normalizeFittness(): # normalizes the fittness value to 1, don't really need it
#     global Fittness
#     sum = 0

#     for i in Fittness:
#         sum += i
    
#     for i in range(len(Fittness)):
#         Fittness[i] = Fittness[i] / sum

# swaps 2 elements with eachother
def swapElements(array, element1, element2):
    temp = array[element1]
    array[element1] = array[element2]
    array[element2] = temp

# calculates the total distance of the city given a specific order and return it
def calculateDistance(CityArray, OrderIndex):
    dist = 0
    
    for i in OrderIndex[: len(CityArray) - 1]:
        tempi = OrderIndex.index(i) + 1
        nexti = OrderIndex[tempi]
        
        currCity = CityArray[i]
        nextCityTemp = CityArray[nexti]
        
        dist += math.sqrt((currCity[0] - nextCityTemp[0])**2 + (currCity[1] - nextCityTemp[1])**2) # does same thing as math.dist() function below, pick one or other, doesn't matter
        
    endCity, StartCity = OrderIndex[len(OrderIndex) - 1], OrderIndex[0] # adds the distance from the last city to the first city at the end

    dist += math.dist(CityArray[endCity], CityArray[StartCity])

    return dist

if __name__ == '__main__':
    main()
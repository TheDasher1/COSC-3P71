import math, random, itertools, re
# import matplotlib.pyplot as plt


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
    random.seed(1)

    try:
        readFile = open('D:\\COSC 3P71\\Term Project\\Assignment 2\\Ulysses22.txt', 'r')

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
        
        #for i in range(13):
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

    except FileNotFoundError as err:
        print(f'File not found. {err}')
    
    except ValueError as err:
        print(f'Invalid input in file, expect only int. {err}')

    print(CityList)
    # print(f'Order before shuffle: {CityIndex}')
    # random.shuffle(CityIndex)
    # print(f'Order after shuffle: {CityIndex}')

    PopSize = None

    while PopSize == None:
        try:
            PopSize = int(input('Enter a population size: '))
            maxGens = int(input('Enter the number of generations to have: '))
        
        except ValueError as err:
            print(f'Invalid input. {err}')
    
    CrossOption = -1

    while CrossOption < 1 or CrossOption > 2:
        try:
            CrossOption = int(input('Enter 1 to use UniformCrossover, or 2 to use two point crossover: '))

        except ValueError as err:
            print(f'Invalid input. {err}')

    while CrossOverProb > 1 or CrossOverProb < 0:
        try:
            CrossOverProb = float(input('Enter rate of crossover as a number between 0 and 1: '))
        
        except ValueError as err:
            print(f'Invalid input. {err}')

    while RateOfMutation > 1 or RateOfMutation < 0:
        try:
            RateOfMutation = float(input('Enter rate of mutation as a number between 0 and 1: '))
        
        except ValueError as err:
            print(f'Invalid input. {err}')

    # PermutedIndexes =  list(itertools.permutations(CityIndex))

    # for i in range(100):
    while len(Population) < PopSize:
        temp = CitiesOrder.copy()

        random.shuffle(temp)

        if temp not in Population:
            Population.append(temp)
    
    # print(f"Total distance travelled for first route: {round(calculateDistance(CityList, CityIndex), 2)}")

    # ------------------------- MAIN Function/loop that does everything ----------------------------
    # while True:
    for i in range(maxGens):
        calculateFittness()
        normalizeFittness()
        bestFittness, averageFittness = findBestFittness()
        print(f"Best fittness of Generation {i} is {bestFittness} and average of fittness of this generation is {averageFittness}")
        makeNextGen(RateOfMutation, CrossOverProb, CrossOption)
    
    print(f'\nBest route: {bestOrder} with distance: {round(bestDistance, 2)}')

def makeNextGen(MutationRate, CrossOverProbability, crossOverOption):
    global Population, NewPopulation, Fittness, CityList
    NewPopulation = []

    # ------------ new way to order fittness or something, think about this hard when you get back to it, something about comparing against the best order of this generation to make the next one or was it to create a fittness value? dunno think really hard about this
    # bestOfCurrentGen = None
    # initDist = calculateDistance(CityList, Population[0])

    # for i in range(len(Population)):
    #     tempGen = Population[i].copy()
    #     currDist = calculateDistance(CityList, tempGen)
    #     if tempDist < currDist:
    #         tempDist = None
    #     findBestOrderOfGen(tempGen)
    # --------------------------------------------------------

    if crossOverOption == 1:
        for i in range(math.ceil(PopSize / 2)): # div by 2 since there will be 2 children inserted into the new generation
            # NewPopulation.append(i.copy())
            
            # ---- if partent1 and partent2 dont work, uncomment this below
            #tempOrder = ChooseOne(Population, Fittness)
            
            # This is the method to select 2 random parents based on their fittness value
            parent1 = ChooseOne(Population, Fittness)
            parent2 = ChooseOne(Population, Fittness)

            # This method will select 2 parents and subject them to a tournement and select them to be crossovered
            # parent1 = tournamentSelection(Population, k)
            # parent2 = tournamentSelection(Population, k)

            # tempOrder = CrossOver(parent1, parent2)
            childOrder1, childOrder2 = UniformOrderCrossOver(parent1, parent2, CrossOverProbability)

            # mutateOrder(tempOrder, MutationRate)
            mutateOrder(childOrder1, MutationRate)
            mutateOrder(childOrder2, MutationRate)
            
            # NewPopulation.append(tempOrder.copy())
            NewPopulation.append(childOrder1.copy())
            NewPopulation.append(childOrder2.copy())
    
    else:
        for i in range(math.ceil(PopSize / 2)): # div by 2 since there will be 2 children inserted into the new generation
            # This is the method to select 2 random parents based on their fittness value
            parent1 = ChooseOne(Population, Fittness)
            parent2 = ChooseOne(Population, Fittness)

            childOrder1, childOrder2 = twoPointCrossOver(parent1, parent2, CrossOverProbability)

            # mutateOrder(tempOrder, MutationRate)
            mutateOrder(childOrder1, MutationRate)
            mutateOrder(childOrder2, MutationRate)
            
            # NewPopulation.append(tempOrder.copy())
            NewPopulation.append(childOrder1.copy())
            NewPopulation.append(childOrder2.copy())

    Population = [] # scraps the old generation and sets the new generation as the current population
    Population = NewPopulation.copy()

def twoPointCrossOver(Parent1, Parent2, crossOverProb):
    Child1 = []
    Child2 = []
    rand = random.random()

    if rand <= crossOverProb: # only performs a crossover if the random chance is <= the probability
        start = random.randrange(0, len(Parent1))
        end = random.randrange(start, len(Parent1))
        Child1 = Parent1[start: end].copy()

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

    else: # else just returns the parents
        return Parent1.copy(), Parent2.copy()

def UniformOrderCrossOver(Parent1, Parent2, crossOverProb):
    rand = random.random()

    if rand <= crossOverProb: # only performs a crossover if the random chance is <= the probability
        mask = []
        Child1, Child2 = [], []
        
        for i in range(len(Parent1)):
            mask.append(random.choice((0, 1)))
        
        for i in range(len(mask)):
            if mask[i] == 1:
                getParent1 = Parent1[i]
                getParent2 = Parent2[i]

                Child2.append(getParent1)
                Child1.append(getParent2)

            else:
                # Child2[i].append(Parent1.index(-1))
                # Child1[i].append(Parent2.index(-1))
                # Child2[i] = -1
                # Child1[i] = -1
                Child2.append(-1)
                Child1.append(-1)
        
        repairGenes(Child1, Child2, Parent1, Parent2)

        return Child1.copy(), Child2.copy()

    else: # else just returns the parents
        return Parent1.copy(), Parent2.copy()

def repairGenes(Child1, Child2, Parent1, Parent2):
    counter = 0
    emptySlots = []

    # ------- Repairs child 1 genes -----------
    for i in range(len(Child1)):
        if Child1[i] == -1:
            emptySlots.append(i)
        
        # counter += 1
    
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
        
        # counter += 1
    
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

    for i in arena:
        dist = calculateDistance(CityList, i)
        fitt = 1 / dist
        
        if fitt > bestFit:
            bestFit = fitt
            OrderToReturn = i.copy()

    return OrderToReturn.copy()

# def tournamentSelection(Popul, k):
#     global PopSize, Fittness
#     best = None

#     for i in range(k):
#         ind = Popul[random.randint(0, PopSize - 1)]

#         if best == None or Fittness[ind] > Fittness[best]:
#             best = ind
    
#     return best

def mutateOrder(Order, rate):
    for i in range(len(CityList)):
        rand = random.random()

        if rand <= rate:
            index1 = math.floor(random.randrange(0, len(Order) - 1))
            index2 = math.floor(random.randrange(0, len(Order) - 1))

            swapElements(Order, index1, index2)

def findBestFittness():
    global Fittness
    # compareFittness = Fittness[0] # sets an initial fittness value to compare all others against
    bestFittness = Fittness[0] #compareFittness # also assigns a best value discovered
    averageFittness = 0

    for i in Fittness:
        if i < bestFittness:
            # compareFittness = i
            bestFittness = i
        averageFittness += i

    averageFittness = averageFittness / len(Fittness)

    return bestFittness, averageFittness

def findBestOrderOfGen(ArrayOrder): # closer it is to last generation's best distance, the higher its fittness value
    pass

def ChooseOne(list, prob):
    index = 0
    rand = random.random()

    while rand > 0:
        rand = rand - prob[index]
        index += 1
    
    index -= 1

    return list[index].copy()

def calculateFittness(): # original algorithm was to calculate how close the current orders to the last generations best distance and assign a fitness value based on that but this works better
    global bestDistance, Fittness, bestOrder, CityList
    Fittness = []

    for i in Population:
        distance = calculateDistance(CityList, i)
        Fittness.append(1 / distance)

        if distance < bestDistance:
            bestDistance = distance
            bestOrder = i.copy()

            print(f'\n{bestOrder} with a distance of {round(bestDistance, 2)}\n')

def normalizeFittness():
    global Fittness
    sum = 0

    for i in Fittness:
        sum += i
    
    for i in range(len(Fittness)):
        Fittness[i] = Fittness[i] / sum

def swapElements(array, element1, element2):
    temp = array[element1]
    array[element1] = array[element2]
    array[element2] = temp

def calculateDistance(CityArray, OrderIndex):
    if len(OrderIndex) != len(CityArray):
        return 'Incorrect length of array and given order.'

    else:
        dist = 0
        # mathDist = 0

        for i in OrderIndex[: len(CityArray) - 1]:
            tempi = OrderIndex.index(i) + 1
            nexti = OrderIndex[tempi]
            
            currCity = CityArray[i]
            nextCityTemp = CityArray[nexti]
            
            dist += math.sqrt((currCity[0] - nextCityTemp[0])**2 + (currCity[1] - nextCityTemp[1])**2) # does same thing as math.dist() function below, pick one or other, doesn't matter
            
            # mathDist += math.dist(currCity, nextCityTemp) # does same thing as math.sqrt() function above, pick one or other, doesn't matter

        endCity, StartCity = OrderIndex[len(OrderIndex) - 1], OrderIndex[0]

        dist += math.dist(CityArray[endCity], CityArray[StartCity])

    return dist

if __name__ == '__main__':
    main()
import math, random
import tkinter as tk
from tkinter import Tk, messagebox
import time, threading
import itertools, re

WIDTH = 600
HEIGHT = 600

global CityList, CityIndex
CityList = []
CityIndex = []

def main():

    try:
        readFile = open('D:\\COSC 3P71\\Term Project\\Assignment 2\\Ulysses22.txt', 'r')

        for i in range(9):
            charIndex = readFile.read(1) # reads it as 2 characters instead of 1 because 2 digit numbers
            
            if charIndex == '': # Might not need this line since for loop is used instead of while loop
                break
            
            CityIndex.append(int(charIndex) - 1) # - 1 for indexing in 0 based list

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
            
            CityIndex.append(int(charIndex) - 1) # - 1 for indexing in 0 based list

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

    canv = tk.Canvas(master=window, width=600, height=500, bg='black')
    canv.propagate(False)
    canv.pack()
    
    numCitiesLable = tk.Label(master=window, text='Enter the number of cities to visit')
    numCitiesChoise = tk.Entry(master=window, width=10)
    numCitiesLable.place(x=10, y=520)
    numCitiesChoise.place(x=192, y=521)

    cittiesGetter = tk.Button(master=window, text='Enter', width=5, height=1, command=lambda: startProblem(CityList, CityIndex, canv)).place(x=260, y=520)
    
    global StartedThread
    StartedThread = False

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    
    
def mainTSPAlgo(numCities, CitiesIndex, canv):
    CityList = []
    CityRep = []
    random.seed(1)

    canv.delete('all') # clears the board

    for i in numCities: # creates cities at random locations and stores them in a list
        temp = (i[0], i[1])
        
        if temp not in CityList: # only adds to the list if the city location doesn't exist in the list
            CityList.append(temp)
            
            # cityRep = tk.Frame(master=window, width=4, height=4, bg='white')
            # cityRep.place(x=temp[0], y=temp[1])

    for i in CityList: # draws the cities on the the UI, the cities will be represented as a small white circle/dot
        # tempFrame = tk.Frame(master=window, width=4, height=4, bg='white').place(x=i[0], y=i[1])
        tempRep = canv.create_rectangle(i[0] - 3, i[1] - 3, (i[0] + 3), (i[1] + 3), fill='white')
        CityRep.append(tempRep)

    # drawLineBetweenPoints(CityList, canv)

    tk.Button(master=window, text='Calculate Best Route', command= lambda: startInThread(CityList, canv)).place(x=280, y=555)

def startInThread(CityList, canvas):
    global stop_event#, StartedThread
    
    stop_event = threading.Event()

    t = threading.Thread(target=TSPALGO, args=(CityList, canvas))
    StartedThread = True
    t.start()

def on_closing():
    # StartedThread = False
    #if messagebox.askokcancel("Quit", "Exit?"):
    if StartedThread:
        stop_event.set()
    window.destroy()

def TSPALGO(CitiesRepresentation, canvBoard):
    dist = 0
    bestDist = 0
    bestRoute = []
    
    drawLineBetweenPoints(CitiesRepresentation, canvBoard)
    
    print(f'Started with: {CitiesRepresentation}')
    
    dist = calcDistanceBetweenCities(CitiesRepresentation)
    bestDist = dist

    # gets permutations of the list of cities
    permutedLocations = list(itertools.permutations(CitiesRepresentation))

    for i in permutedLocations:
        if stop_event.is_set():
            break
        
        # CitiesRepresentation = swapCities(CitiesRepresentation, random.randint(0, len(CitiesRepresentation) - 1), random.randint(0, len(CitiesRepresentation) - 1))#notsameRandom(len(CitiesRepresentation) - 1))
        dist = calcDistanceBetweenCities(i)
        
        drawLineBetweenPoints(i, canvBoard)

        # drawBestRoute(bestRoute, canvBoard) # draws a line between the current best route
        
        if dist < bestDist:
            bestDist = dist
            bestRoute = i
            print(f'Current best Route: {bestRoute} with distance: {round(bestDist, 2)}')
        
        

    print(f'\nFinished with {bestRoute} and a distance of {(round(bestDist, 2))}\n')
    drawBestRoute(bestRoute, canvBoard)

def calcDistanceBetweenCities(CitiesArray):
    dist = 0
    
    for cit in CitiesArray[: len(CitiesArray) - 1]:
        nextCityTemp = CitiesArray[CitiesArray.index(cit) + 1]
        dist += math.sqrt((cit[0] - nextCityTemp[0])**2 + (cit[1] - nextCityTemp[1])**2)

    return dist

def swapCities(citiesArray, city1, city2):
    temp = citiesArray[city1]
    citiesArray[city1] = citiesArray[city2]
    citiesArray[city2] = temp

    return citiesArray

def swapCitiesTuple(citiesArray, cityTuple):
    # ind1 = citiesArray[city1]
    # ind2 = citiesArray[city2]

    temp = citiesArray[cityTuple[0]]
    citiesArray[cityTuple[0]] = citiesArray[cityTuple[1]]
    citiesArray[cityTuple[1]] = temp

    return citiesArray

# def swapCitiesWithIndex(cittiesArray, city1, city2):
#     ind1 = cittiesArray.index(city1)
#     ind2 = cittiesArray.index(city2)

#     temp = cittiesArray[ind1]
#     cittiesArray[ind1] = cittiesArray[ind2]
#     cittiesArray[ind2] = temp

#     return cittiesArray

def drawBestRoute(board, boardcanvas):
    boardcanvas.delete('all')
    
    for i in board[:len(board) - 1]:
        destination = board[board.index(i) + 1]
        boardcanvas.create_rectangle(i[0] - 3, i[1] - 3, (i[0] + 3), (i[1] + 3), fill='blue') # Rectangle to represent the City
        boardcanvas.create_line(i[0], i[1], destination[0], destination[1], fill='blue', width=7) # Line that will be drawn between the cities


def drawLineBetweenPoints(points, canv): # draws a line between the points in the given order on the Canvas
    canv.delete('all')
    
    for i in points[:len(points) - 1]:
        destination = points[points.index(i) + 1]
        canv.create_rectangle(i[0] - 3, i[1] - 3, (i[0] + 3), (i[1] + 3), fill='white')
        canv.create_line(i[0], i[1], destination[0], destination[1], fill='white')
    
    # temp = len(points) --------- Does not work correctly ------ Fix later --------------

    # canv.create_rectangle(temp - 3, temp - 3, (temp + 3), (temp + 3), fill='white') # draws the last dot to represent the last city sperately since the above loop only goes to the second last city

def startProblem(CityLists, CityIndexs, canv):
    # temp = field.get()
    
    # mainTSPAlgo(int(temp), canv)
    mainTSPAlgo(CityLists, CityIndexs, canv)
    
def notsameRandom(len):
    num1, num2 = 0, 0

    while num1 == num2:
        num1, num2 = random.randint(0, len), random.randint(0, len)

    return (num1, num2)

window = tk.Tk()

window.title('TSP Problem')
window.configure(bg='gray')
window.geometry(f"{WIDTH}x{HEIGHT}+{700}+{50}")
window.resizable(width=False, height=False)

if __name__ == '__main__':
    main()
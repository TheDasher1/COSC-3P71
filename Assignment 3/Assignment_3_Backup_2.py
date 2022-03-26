import numpy as np
import random, math, itertools
import NueronLayer as NL

#
#    8 hidden layers
#         
#         O----
#     ----O----
#   O-----O----         
#   O-----O----    O  <---- Output layer (single output)
#   O-----O----
#   O-----O----
#     ----O----
#         O----
#
#

def main():
    numEpochs = 0
    bestLoss = math.inf
    
    # while numEpochs <= 0:
    #     try:
    #         numEpochs = int(input("Number of Epochs to run for: "))

    #     except ValueError as err:
    #         print(f"Invalid input. {err}")

    X = np.array([ # 2^4 = 16 different combinations are all created here
                  [0, 0, 0, 0],
                  [0, 0, 0, 1],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [1, 0, 0, 0],
                  [0, 0, 1, 1],
                  [0, 1, 1, 0],
                  [1, 1, 0, 0],
                  [1, 0, 0, 1],
                  [1, 0, 1, 0],
                  [0, 1, 0, 1],
                  [1, 0, 1, 1],
                  [0, 1, 1, 1],
                  [1, 1, 0, 1],
                  [1, 1, 1, 0],
                  [1, 1, 1, 1]
                  ]) # 16 X 4 matrix (16 rows, 4 columns)

    actualValues = np.array([
                          [1],
                          [0], 
                          [0], 
                          [0], 
                          [0], 
                          [1], 
                          [1], 
                          [1], 
                          [1], 
                          [1], 
                          [1], 
                          [0], 
                          [0], 
                          [0], 
                          [0], 
                          [1]
                        ])

    np.random.seed(1) # uncomment if results need to be replicable
    inputLayerSize = 4 # 4 input numbers, (0 1 0 1, 1 0 0 1, 1 1 1 0, etc.)
    hiddenLayerSize = 8 # 1 hidden layer with a given number of neurons
    outputLayerSize = 1 # 1 output node, either a 0 or 1

    # layerSize = (inputSize, hiddenLayerSize, outPutSize)
    # weight_shapes = [(a, b) for a, b in zip(layerSize[1: ], layerSize[: -1])]
    # print(weight_shapes, ' weight shapes\n')

    # weights = [np.random.standard_normal(s) for s in weight_shapes]
    # biases = [np.zeros((s, 1)) for s in layerSize[1: ]] # inits all biases to 0

    # for w in weights:
    #     print(w, '\n')

    # inputLayer = [0, 0, 0, 1] # 4 X 1 layer matrix of inputs
    # weightsLayer = [] # will be a 8 X 4 layer matrix that will later be populated with random default values as weights
    # temp = []
    # biasesLayer = np.zeros(hiddenLayerSize, dtype=int) # inits a 8 X 1 layer of biases as an array of 0's

    # populates the 
    # for i in range(hiddenLayerSize):
    #     for j in range(len(inputLayer)):
    #         # w = random.randint(-3, 3)
    #         w = np.random.standard_normal() # values for a normal distribution chart are generated
    #         temp.append(w)
    #     weightsLayer.append(temp.copy())
    #     temp = []

    # num = 1
    # for wl in weightsLayer:
    #     print(f'Neuron {num} in hidden layer: {wl} with bias: {biasesLayer[num - 1]}')
    #     num += 1

    # print(biasesLayer)

    # zipED = zip(weightsLayer, biases)

    # for z in zipED:
    #     print(z)

    # OPLayer = []
    # for neuronWeights, neuronBiases in zip(weightsLayer, biasesLayer):
    #     neuronOP = 0

    #     for nInput, weigh in zip(inputLayer, neuronWeights):
    #         neuronOP += nInput * weigh

    #     neuronOP += neuronBiases

    #     OPLayer.append(neuronOP)

    # print(OPLayer)

    # outPutNPV = np.dot(weightsLayer, inputLayer) + biasesLayer # matrix multiplication using np library
    # #                   8 X 4         4 X 1

    # print(outPutNPV)

    # OPNPV = np.dot(weightsLayer, le) + biasesLayer # will not work since matrices are not aligned
    # #                8 X 4       16 X 4

    # print(OPNPV)

    # TPNPV = np.dot(le, np.transpose(weightsLayer)) + biasesLayer

    # print(f"{X}\n")
    # print(weightsLayer, "\n")
    # print(TPNPV)

    XLayer = NL.NeuronLayer(inputLayerSize, hiddenLayerSize) # 4 is in the input layer position to represent the 4 digits being inputted, and 8 in the neuron layer to represent 8 neurons
    HiddenLayer = NL.NeuronLayer(hiddenLayerSize, outputLayerSize) # 8 in the input layer position to represent the 8 inputs being given to it by the input layer, and 1 digit in the neuron layer to represent the if its even or odd

    # IPLayerRT = FirstLayer.forwardPass(X)
    XLayer.forwardPass(X) # performs forwards pass on the input of 0s and 1s to the hidden neuron layer and stores the outPut in the class
    # print(IPLayerRT)

    print(f"\nWeights from the {inputLayerSize} input neurons towards the {hiddenLayerSize} hidden neurons: \n{XLayer.weights}\n")
    
    counter = 0
    for n in XLayer.outPut:
        print(f"Input {counter + 1}\tCombination of 0s and 1s: {X[counter]}\t\nOutput(value given/held by the {hiddenLayerSize} hidden neurons): {n}\n")
        counter += 1
    
    # print(np.sum(np.exp(X - np.max(X, axis=1, keepdims=True)), axis=1, keepdims=True))

    ActivHideLayer = XLayer.outPut # the hidden layer's weights

    # applies the sigmoid function to all the weights in the hidden layer
    for y in range(len(ActivHideLayer)):
        for x in range(len(ActivHideLayer[y])):
            temp = ActivHideLayer[y][x]
            
            t = activationFunction(temp)
            
            ActivHideLayer[y][x] = t
    
    print(ActivHideLayer)
    # Y.forwardPass(activationFunction(FirstLayer.outPut)) # performs forward pass on the output that the Neurons in the hidden layer have, this will be the final value that is supposed to guess if even or odd
    
    HiddenLayer.forwardPass(ActivHideLayer)
    
    print(f"\nWeights from the {hiddenLayerSize} input neurons towards the {outputLayerSize} hidden neurons: \n{HiddenLayer.weights}\n")
    
    print(f"Y output: \n{HiddenLayer.outPut}\n")

    Y = HiddenLayer.outPut

    # applies the sigmoid function to all the weights in the hidden layer
    for y in range(len(Y)):
        for x in range(len(Y[y])):
            temp = Y[y][x]
            
            t = activationFunction(temp)
            
            Y[y][x] = t
    
    print(f"Y Sigmoid: \n{Y}")

    MSE = np.square(np.subtract(actualValues, Y)).mean()
    
    print(MSE)

    # Layer1 = 
    # for i in range(numEpochs):


# Logistic Activation function(Sigmoid Function)
def activationFunction(x):
    # for y in range(len(x)):
    #     for x in range(len(x[y])):
    #         x[y][x] = 1 / (1 + math.exp(-x[y][x]))
    
    # return x

    return 1 / (1 + math.exp(-x))

if __name__ == '__main__':
    main()
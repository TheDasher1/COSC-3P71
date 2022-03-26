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

    # np.random.seed(1) # uncomment if results need to be replicable
    inputLayerSize = 4 # 4 input numbers, (0 1 0 1, 1 0 0 1, 1 1 1 0, etc.)
    hiddenLayerSize = 8 # 1 hidden layer with a given number of neurons
    outputLayerSize = 1 # 1 output node, either a 0 or 1

    iSent = 6
    globalLoss = math.inf

    X_Input_Layer_To_Hidden_Layer_Weights_Biases = NL.NeuronLayer(inputLayerSize, hiddenLayerSize) # 4 is in the input layer position to represent the 4 digits being inputted, and 8 in the neuron layer to represent 8 neurons
    
    Hidden_Layer_To_Y_Output_Layer_Weights_Biases = NL.NeuronLayer(hiddenLayerSize, outputLayerSize) # 8 in the input layer position to represent the 8 inputs being given to it by the input layer, and 1 digit in the neuron layer to represent the if its even or odd

    X_Input_Layer_To_Hidden_Layer_Weights_Biases.forwardPass(X[iSent]) # performs forwards pass on the input of 0s and 1s to the hidden neuron layer and stores the outPut in the class
    
    print(f"\nWeights from the {inputLayerSize} input neurons towards the {hiddenLayerSize} hidden neurons: \n{X_Input_Layer_To_Hidden_Layer_Weights_Biases.weights}\n")
    
    # counter = 0
    # for n in X_Input_Layer_To_Hidden_Layer_Weights_Biases.outPut:
    #     print(f"Input {counter + 1}\tCombination of 0s and 1s: {X[counter]}\t\nOutput(value given/held by the {hiddenLayerSize} hidden neurons): {n}\n")
    #     counter += 1
    
    Activation_Of_Hidden_Layer = SendActivation(X_Input_Layer_To_Hidden_Layer_Weights_Biases.outPut) # the hidden layer's weights

    # applies the sigmoid function to all the weights in the hidden layer
    # for y in range(len(ActivHiddenLayer)):
    #     for x in range(len(ActivHiddenLayer[y])):
    #         temp = ActivHiddenLayer[y][x]
            
    #         t = activationFunction(temp)
            
    #         ActivHiddenLayer[y][x] = t
    
    print(f"{hiddenLayerSize} Hidden layer's activation: {Activation_Of_Hidden_Layer}")
    # Y.forwardPass(activationFunction(FirstLayer.outPut)) # performs forward pass on the output that the Neurons in the hidden layer have, this will be the final value that is supposed to guess if even or odd
    
    Hidden_Layer_To_Y_Output_Layer_Weights_Biases.forwardPass(Activation_Of_Hidden_Layer)
    
    print(f"\nWeights from the {hiddenLayerSize} input neurons towards the {outputLayerSize} hidden neurons: \n{Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights}\n")
    
    print(f"Y weights output: \n{Hidden_Layer_To_Y_Output_Layer_Weights_Biases.outPut}\n")

    Y_Output_Activation = SendActivation(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.outPut)

    # applies the sigmoid function to all the weights in the hidden layer
    # for y in range(len(Y)):
    #     for x in range(len(Y[y])):
    #         temp = Y[y][x]
            
    #         t = activationFunction(temp)
            
    #         Y[y][x] = t
    
    print(f"Y Activation: {Y_Output_Activation}\nShould be: {actualValues[iSent]}")

    globalLoss = getLoss(actualValues[iSent], Y_Output_Activation)#np.square(np.subtract(actualValues, Y)).mean()
    
    print(f"Loss: {globalLoss}\n")

    # for i in range(numEpochs):
    # global loss (the error) is a scaler
    # hiddenLayerWeightssErrors = np.dot(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights, globalLoss)
    # print(hiddenLayerWeightssErrors)
    tempOutputs = Y_Output_Activation * (1 - Y_Output_Activation)
    

    # Layer1Weights = XLayer.weights.copy()
    # Layer1Biases = XLayer.biases.copy()
    # Layer2Weights = HiddenLayer.weights.copy()
    # Layer2Biases = HiddenLayer.biases.copy()

    # for i in range(numEpochs):
    #     XLayer.weights = np.random.uniform(low=-1, high=1, size=(inputLayerSize, hiddenLayerSize))
    #     XLayer.biases = np.random.uniform(low=-1, high=1, size=(1, hiddenLayerSize))

    #     HiddenLayer.weights = np.random.uniform(low=-1, high=1, size=(hiddenLayerSize, outputLayerSize))
    #     HiddenLayer.biases = np.random.uniform(low=-1, high=1, size=(1, outputLayerSize))

    #     XLayer.forwardPass(X)
    #     ActivHiddenLayer = SendActivation(XLayer.outPut)
        
    #     HiddenLayer.forwardPass(ActivHiddenLayer)
    #     YLayer = SendActivation(HiddenLayer.outPut)

    #     loss = getLoss(actualValues, YLayer)

    #     if loss < bestLoss:
    #         print(f"New set of weights and biases found on itteration {i + 1} with loss of {loss}")

    #         Layer1Weights = XLayer.weights.copy()
    #         Layer1Biases = XLayer.biases.copy()
    #         Layer2Weights = HiddenLayer.weights.copy()
    #         Layer2Biases = HiddenLayer.biases.copy()

    #         bestLoss = loss

def getLoss(ActualValues, CalculatedValues):
    return np.square(np.subtract(ActualValues, CalculatedValues)).mean()

def SendActivation(XArray):
    for y in range(len(XArray)):
        for x in range(len(XArray[y])):
            temp = XArray[y][x]
            
            t = activationFunction(temp)
            
            XArray[y][x] = t
    
    return XArray

# Logistic Activation function(Sigmoid Function)
def activationFunction(x):
    return 1 / (1 + math.exp(-x))

if __name__ == '__main__':
    main()
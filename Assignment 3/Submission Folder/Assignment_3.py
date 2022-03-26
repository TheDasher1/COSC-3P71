import numpy as np
import random, math
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
    # initial values
    numEpochs = 0
    learningRate = 0.0
    outPutTime = 0
    acceptbleLoss = 0.0
    
    # set up the default values
    while numEpochs <= 0:
        try:
            numEpochs = int(input("Number of Epochs to run for: "))

        except ValueError as err:
            print(f"Invalid input. {err}")

    while learningRate <= 0.0:
        try:
            learningRate = float(input("Enter the learning rate: "))

        except ValueError as err:
            print(f"Invalid input. {err}")
    
    while outPutTime <= 0:
        try:
            outPutTime = int(input("How many iterations to output MSE: "))
        
        except ValueError as err:
            print(f"Invalid input. {err}")

    while acceptbleLoss <= 0.0:
        try:
            acceptbleLoss = float(input("Enter an acceptable loss value: "))

        except ValueError as err:
            print(f"Invalid input. {err}")

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

    # actual values to compare the OP of the NN against
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

    iSent = random.randint(0, 15)
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
    
    # performs forward pass on the output that the Neurons in the hidden layer have, this will be the final value that is supposed to guess if even or odd
    print(f"{hiddenLayerSize} Hidden layer's activation: {Activation_Of_Hidden_Layer}")
    
    Hidden_Layer_To_Y_Output_Layer_Weights_Biases.forwardPass(Activation_Of_Hidden_Layer)
    
    print(f"\nWeights from the {hiddenLayerSize} input neurons towards the {outputLayerSize} hidden neurons: \n{Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights}\n")
    
    print(f"Y weights output: \n{Hidden_Layer_To_Y_Output_Layer_Weights_Biases.outPut}\n")

    # applies the sigmoid function to all the weights in the hidden layer
    Y_Output_Activation = SendActivation(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.outPut)

    print(f"Y Activation: {Y_Output_Activation}\nShould be: {actualValues[iSent]}")

    globalLoss = getLoss(actualValues[iSent], Y_Output_Activation)
    
    print(f"Loss: {globalLoss}\n")

    counter = 0 # used to OP MSE

    # there are times where I mostly understand what this is doing, those are rare, mostly I just feel really stupid, I follow whats happening on paper with calculus but here, I THINK I know whats happening, but maybe not, I've watched 3blue1brown's vid a couple of times now and read a lot on this topic, but this just hurts my brain
    for i in range(numEpochs):
        sent = random.randint(0, 15)

        # sends a random element in the list of inputs to performs back propigation on
        X_Input_Layer_To_Hidden_Layer_Weights_Biases.forwardPass(X[sent])
        
        # ------------ Performs the calculations on the Input weights towards the hidden layer ----------------
        #calculates the derivative of all the weights in this matrix
        gradientsOutputs = derivSigmoids(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights) # have to adjust the weights, cant mess with the activation values directly
        
        # multiplies all the derivative values with the loss value
        tempWeights = np.dot(gradientsOutputs, globalLoss)

        # multiplies all the values in the matrix with the learning rate
        gradientsOutputs = np.dot(tempWeights, learningRate)
        
        # transposes the weights to be multiplied with the delta of output
        hiddenT = np.transpose(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights)

        # multiplies the gradiante of the outputs with the transpose to get the delta of the weights
        weightsHODeltas = np.dot(gradientsOutputs, hiddenT)

        # temp hold of the matrix of weights of the current matrix
        lastHiWei = Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights

        # adds the last layer and the delta of the weights and adjust the weights of the matrix (should be + or -)
        Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights = np.add(lastHiWei, weightsHODeltas)
        # this also changes the biases with the delta
        Hidden_Layer_To_Y_Output_Layer_Weights_Biases.biases = np.add(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.biases, weightsHODeltas)

        # ------------ Performs the same/similar calculations on the hidden weights towards the output layer ----------------
        ho_t = np.transpose(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.weights)
        hid_err = np.dot(ho_t, globalLoss)

        gradientHidden = derivSigmoids(Activation_Of_Hidden_Layer)
        
        hidT = np.dot(gradientHidden, hid_err)

        gradientHidden = np.dot(hidT, learningRate)

        inputT = np.transpose(gradientHidden)

        weightIHDelta = np.dot(gradientHidden, inputT)

        lastihWei = X_Input_Layer_To_Hidden_Layer_Weights_Biases.weights

        X_Input_Layer_To_Hidden_Layer_Weights_Biases.weights = np.add(lastihWei, weightIHDelta)
        X_Input_Layer_To_Hidden_Layer_Weights_Biases.biases = np.add(X_Input_Layer_To_Hidden_Layer_Weights_Biases.biases, weightIHDelta)

        # --------------------------------------------------------------------------------------------------------

        globalLoss = getLoss(actualValues[sent], Y_Output_Activation) # checks the new loss

        if counter == outPutTime: # outputs the MSE if the number of itterations to OP for is reached
            print(f"Iteration: {i}\tMSE: {globalLoss}")
            counter = 0

        # breaks if the loss rate has reached acceptable levels
        if globalLoss <= acceptbleLoss:
            print(f"Loss rate is {globalLoss}")
            break

        counter += 1
    
    # test the NN to see if it has learned anything
    sendIndex = int(input("Index to check: "))

    X_Input_Layer_To_Hidden_Layer_Weights_Biases.forwardPass(X[sendIndex])

    print(f"Calculated: {activationFunction(Hidden_Layer_To_Y_Output_Layer_Weights_Biases.outPut)}\nActual: {actualValues[sendIndex]}")

# returns the derivative of all the elements of a given matrix/array
def derivSigmoids(nArray):
    tempArray = nArray # work on copy just incase
    tempValue = 0

    for y in range(len(tempArray)):
        for x in range(len(tempArray[y])):
            tempValue = tempArray[y][x]
            t = tempValue * (1 - tempValue)
            tempArray[y][x] = t

    return tempArray

# returns the MSE, given the actual value and what the NN has calculated
def getLoss(ActualValues, CalculatedValues):
    return np.square(np.subtract(ActualValues, CalculatedValues)).mean()

# performs the activation of all the elements of the matrix/array
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
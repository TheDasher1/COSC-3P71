import numpy as np
import random

class NeuronLayer:

    # default values
    weights = None
    biases = None
    outPut = None
    
    # ------------------------------------
    # random.seed(1) # not sure if random needs to be seeded to be able to replicate results
    # np.random.seed(1)
    # ------------------------------------

    # initial method, it takes inputs and sets up the weigts and biases for this neuron layer, depending on how it is called, it can be a hidden neuron layer or the output layer
    def __init__(self, NumOfInputs, NumOfNeurons):
        self.weights = np.random.uniform(low=-1, high=1, size=(NumOfInputs, NumOfNeurons)) # inits the weight matrix with values between -1 and 1
        self.biases = np.zeros((1, NumOfNeurons)) # inits the bias layer as a matrix of 0s

    # performs forward pass on a given input with weights that were previously calculated
    # calculates the dot product of the given input and weigts of this neuron and adds the bias then returns the result
    def forwardPass(self, input):
        self.outPut =  np.dot(input, self.weights) + self.biases # matrix multiplication of the given input with the weights and then adds the bias values

        return self.outPut # returns the result of the forward pass if it needs to be stored, otherwise calling the output for this class will return it to be used

import os
import tensorflow as tf
import numpy as np

class DeepQNetwork(object):

    def __init__(self, name, learningRate, numActions, inputDimensions, layerDims=256, saveDir="C:/Temp/WifiRouter"):
        
        self.name = name                                            # We use this to allow for multiple networks in tf
        
        self.alpha = learningRate                                   # The rate at which the network will learn at
        self.numActions = numActions                                # The number of actions that the network can decide on
        self.inputDimensions = inputDimensions                      # The number of inputs for the network
        self.layerDims = layerDims                                  # The number of tensors in each layer
        self.saveDir = saveDir
        
        self.session = tf.Session()                                 # Our current tensorflow session that stores the network
        self.CreateNetwork()                                        # Create the network

        self.session.run(tf.global_variables_initializer())         # Run the network

        self.saver = tf.train.Saver()                               # Store the saver function for future use
        self.saveFile = os.path.join(saveDir, "DeepQ.ckpt")         # Get the path to the checkpoint file

    def CreateNetwork(self):
        
        with tf.variable_scope(self.name):

            self.inputNetwork = tf.placeholder(tf.float32, shape=[None, *self.inputDimensions], name="inputs")  # Our input network
            self.actionNetwork = tf.placeholder(tf.float32, shape=[None, *self.numActions], name="actions")     # Our action network
            self.qTargetNetwork = tf.placeholder(tf.float32, shape=[None, *self.numActions], name="qValues")    # Our q target network

            flat = tf.layers.flatten(self.inputNetwork) # Flatten the input network
            firstLayer = tf.layers.dense(flat, units=self.layerDims, activation=tf.nn.relu) # The First layer of the network
            secondLayer = tf.layers.dense(firstLayer, units=self.layerDims, activation=tf.nn.relu) # The second layer of the network

            self.qValueNetwork = tf.layers.dense(secondLayer, units=self.numActions) # Our complete deep Q network with out actions as outputs

            self.loss = tf.reduce_mean(tf.square(self.qValueNetwork - self.qNetwork)) # Get our current loss after initializing
            self.trainOperation = tf.train.AdamOptimizer(self.alpha).minimize(self.loss) # Perform a training operation on the network

    def LoadSave(self):
        print("Loading save...")
        self.saver.restore(self.session, self.saveFile)

    def CreateSave(self):
        self.saver.save(self.session, self.saveFile)
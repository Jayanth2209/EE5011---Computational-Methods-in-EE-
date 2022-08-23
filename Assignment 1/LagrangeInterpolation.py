import random
import numpy as numpy
import matplotlib.pyplot as plt
from pylab import *

import os

def CompileCCode(filename, N):
    os.system("gcc -o " + filename + " " + filename + ".c")
    os.system("./" + filename + " " + str(N))

    TEXT = np.loadtxt(filename + ".txt")
    INP = TEXT[:,0] 
    INTOUT = TEXT[:,1]

    return INP, INTOUT

def Plot():

    # Compile the C code
    INP, INTOUT = CompileCCode("LagrangeInterpolation", 0)

    # Data
    X = np.arange(0,2,1e-5)
    Y_ACTUAL = np.sin(np.pi*X)

    # Plotting the actual function and the interpolated function
    title((label = "Actual Values vs Interpolated Values"))
    xlabel(r'$X/\pi \rightarrow$')
    ylabel(r'$\sin(X) \rightarrow$')

    # Plotting the actual function
    plot(X,Y_ACTUAL,label = "Actual Values")

    # Plotting the interpolated function
    plot(INP,INTOUT,label = "Interpolated Values")

    legend()
    savefig("LagrangeInterpolation.png")
    show()

    X_ = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])
    DELTA = X - 




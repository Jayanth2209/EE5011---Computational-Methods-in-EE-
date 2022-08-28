import numpy as numpy
import matplotlib.pyplot as plt
from pylab import *

import os

def CompileCCode(filename, N):
    os.system("gcc -o " + filename + ".out " + filename + ".c")
    os.system("./" + filename + ".out " + str(N))

    TEXT = np.loadtxt("output.txt")
    INP = TEXT[:,0] 
    INTOUT = TEXT[:,1]

    return INP, INTOUT

def Plot():
    # Compile the C code
    INP, INTOUT = CompileCCode("LagrangeInterpolation", 0)

    X = np.arange(0,2,1e-5)     # X Values
   
    Y_ACTUAL = np.sin(np.pi*X)  # Actual Y Values

    # Plotting the Actual function and the Interpolated function
    title(label = "Actual Values vs Interpolated Values")
    xlabel(r"$X/\pi \rightarrow$")
    ylabel(r"$\sin(X) \rightarrow$")

    # Plotting the Actual function
    plot(X, Y_ACTUAL, label = "Actual Values", color = "green", linewidth = 2)

    # Plotting the Interpolated function
    plot(INP, INTOUT, label = "Interpolated Values", color = "blue", linewidth = 4, linestyle = '--')

    legend()
    savefig("LagrangeInterpolation.png")
    show()

    X_ = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])

    DELTA = np.sin(np.pi*INP) - INTOUT
    print("Absolute Error in Interpolation: " + str(np.sum(np.abs(DELTA))))

    # Plotting the Absolute Error in Interpolation
    title(label = "Absolute Error in Interpolation")
    xlabel(r"$X/\pi \rightarrow$")
    ylabel(r"Error $\rightarrow$")
    scatter(X_, np.zeros(len(X_)), marker = 'o', color = "blue")
    semilogy(INP, DELTA, label = "Absolute Error", color = "green")
    legend()
    savefig("LagrangeInterpolationErrorAbs0.png")
    show()

def GaussNoise():

    SIGMA = np.array([0.01, 0.04, 0.07, 0.10, 0.13, 0.16, 0.19, 0.22, 0.25])

    X = np.arange(0,2,1e-5)     # X Values
    Y_ACTUAL = np.sin(np.pi*X)  # Actual Y Values

    plot(X, Y_ACTUAL, label = "Actual Values", color = "black", linewidth = 4, linestyle = "-")
    
    for i in range(9): 
        INP, INTOUT = CompileCCode("LagrangeInterpolation", i+1)
        plot(INP, INTOUT, label = r"$\sigma = $" + str(SIGMA[i]), linewidth = 2, linestyle = "--")
    
    title("Actual Values vs Interpolated Values with Gaussian Noise of Different Variance")
    xlabel(r"$X/\pi \rightarrow$")
    ylabel(r"$\sin(X) \rightarrow$")
    legend()
    savefig("LagrangeInterpolationGaussNoise.png")
    show()

    X_ = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])

    ABSNOISE = []
    for i in range(9):
        INP, INTOUT = CompileCCode("LagrangeInterpolation", i+1)
        DELTA = np.sin(np.pi*INP) - INTOUT
        ABSNOISE.append(np.sum(np.abs(DELTA)))
        scatter(X_, np.zeros(len(X_)), marker = 'o', color = "blue")
        semilogy(INP, DELTA, label = r"$\sigma = $" + str(SIGMA[i]))
    title("Absolute Error in Interpolation for various values of $\sigma$")
    xlabel(r"$X/\pi \rightarrow$")
    ylabel(r"Error $\rightarrow$")
    legend()
    savefig("LagrangeInterpolationErrorAbs1.png")
    show()

    plot(SIGMA, ABSNOISE, label = "Absolute Error vs $\sigma$")
    title("Absolute Error vs " + r"$\sigma$")
    xlabel(r"$\sigma \rightarrow$")
    ylabel(r"Error $\rightarrow$")
    legend()
    savefig("LagrangeInterpolationErrorAbsSigma.png")
    show()

def GenGaussNoise():

    SIGMA = np.array([0.01, 0.04, 0.07, 0.10, 0.13, 0.16, 0.19, 0.22, 0.25])

    X_ = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])
    Y_ = np.sin(np.pi*X_)

    OUT = []
    for sig in SIGMA:
        X = np.random.randn(9)*sig
        Y = list(np.round(Y_ + X, 5))
        OUT.append(Y)
    
    return OUT

#OUT = GenGaussNoise()
#print(OUT)

Plot()
GaussNoise()







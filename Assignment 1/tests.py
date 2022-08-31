from scipy import *
from matplotlib.pyplot import *
import weave

X = linspace(-1,1,10000)
Y = sin(X*pi)/(sqrt(1-X**2))
plot(X, Y, 'k')
show()
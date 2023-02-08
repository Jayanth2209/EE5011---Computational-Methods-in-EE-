# Imports
from scipy import *
from matplotlib.pyplot import *
import weave
from scipy import special

with open("spline.c", "r") as f:
    scode = f.read()


# Function Definition
def f(x):
    return pow(x, (1 + special.j0(x))) / sqrt((1 + (100 * x * x)) * (1 - x))


# Q2 A
x = arange(0.1, 0.95, 0.05)
y = f(x)

# Q2 B
xlabel("x")
ylabel("y = f(x)")
title("Plot of the function f(x)")
plot(x, y)
show()

# Q2 C
h = logspace(-4, -1, 16)
N = (0.8) / h
err = zeros(h.shape)
for i in range(len(h)):
    x = linspace(0.1, 0.9, N[i])
    y = f(x)
    n = int(N[i])
    xx = linspace(0.1, 0.9, 10 * n + 1)
    y2 = zeros(x.size)
    u = zeros(x.size)
    yy = zeros(xx.size)
    code = """
    #include<math.h>
    int i;
    double xp;
    spline(x,y,n,1e30,1e30,y2,u);
    for(i=0;i<=10*n;i++){
        xp=xx[i];
        splint(x,y,y2,n,xp,yy+i);
    }
    """
    weave.inline(code,["x","y","n","y2","u","xx","yy"],\
    support_code=scode,extra_compile_args=["-g"],\
    compiler="gcc")
    if i == 0:
        figure(2)
        plot(x, y, 'ro')
        plot(xx, yy, 'g')
        title("Interpolated values and data points for n=%d" % N[i])
    figure(0)
    z = abs(yy - f(xx))
    plot(xx, z, label="N=%d" % N[i])
    err[i] = z.max()
print(err)

xlabel("x")
ylabel("Error")
legend(loc="upper left")
figure(1)
loglog(h, err)
title("Error vs. Spacing")
xlabel("Spacing")
ylabel("Error")
show()

# Spline Interpolation for 1250 points
h = 0.00064  # 0.8/1250
N = 0.8 / h
err = 0
x = linspace(0.1, 0.9, N)
y = f(x)
n = int(N)
xx = linspace(0.1, 0.9, 10 * n + 1)
y2 = zeros(x.size)
u = zeros(x.size)
yy = zeros(xx.size)
code = """
#include<math.h>
int i;
double xp;
spline(x,y,n,1e30,1e30,y2,u);
for(i=0;i<=10*n;i++){
    xp=xx[i];
    splint(x,y,y2,n,xp,yy+i);
}
"""
weave.inline(code,["x","y","n","y2","u","xx","yy"],\
support_code=scode,extra_compile_args=["-g"],\
compiler="gcc")
figure(0)
plot(x, y, 'ro')
plot(xx, yy, 'g')
title("Interpolated values and data points for n=%d" % N)
show()
z = abs(yy - f(xx))
plot(xx, z, label="N=%d" % N)
err = z.max()
print(err)
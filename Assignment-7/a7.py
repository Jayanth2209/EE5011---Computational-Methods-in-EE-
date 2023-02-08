import numpy as np
import random
from matplotlib import pyplot as plt
#Q1
def genNormalDist(n):
	#generate n independent normally distributed numbers (mean = 0, variance = 1)
	res = []
	for i in range((n+1)//2):
		u1 = np.random.rand()
		u2 = np.random.rand()
		z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2*np.pi*u2)
		z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2*np.pi*u2)
		res.append(z1)
		res.append(z2)
	return np.array(res[0:n])
#histogram for normal distribution
fig, ax = plt.subplots(figsize=(10,7))
ax.hist(genNormalDist(100000),bins = np.linspace(-10,10,1000))
#plt.savefig('histNormal.jpg')
plt.show()
#Q2
def nPacketsTime(n):
	res = 0
	for _ in range(n):
		res += -np.log(1 - np.random.rand())
	return res
#histogram for 30th packet arrival time
fig2, ax2 = plt.subplots(figsize=(10,7))
ax2.hist([nPacketsTime(30) for i in range(100)])
#plt.savefig('hist30th.jpg')
plt.show()
#Q3
#(a)
def f(x,y):
	alpha = np.pi * np.sin(10 * (np.sqrt(x*x + y * y) - 0.5))
	calpha = np.cos(alpha)
	salpha = np.sin(alpha)
	u = x * calpha + y * salpha - 0.5
	v = -x * salpha + y * calpha - 0.5
	return u * u + v * v
#(b)c
fx = np.linspace(-1.5,1.5,100)
fy = np.linspace(-1.5,1.5,100)
[X,Y] = np.meshgrid(fx,fy)
fig3, ax3 = plt.subplots(figsize=(10,7))
Z = np.array([f(x,y) for x,y in zip(X,Y)])
cs = ax3.contourf(X,Y,Z)
cbar = fig3.colorbar(cs)
#plt.savefig('contourQ3.jpg')
plt.show()
fig4, ax4 = plt.subplots(figsize=(10,7))
cs = ax4.contourf(X,Y,Z,vmin=0,vmax=1)
cbar = fig4.colorbar(cs)
#plt.savefig('contourQ3Filtered.jpg')
plt.show()
#(c) |f| < 1 lies in rectangle -2 < x,y < 2
inside = 0
total = int(2e6)
for i in range(total):
	z = f(np.random.uniform(-2,2),np.random.uniform(-2,2))
	inside += int(z < 1)
print("Area is equal to: ", '%.4f' %(16.0 * inside/total))
#Q4
#implementation of poisson distribution with arrival rate lam
def poisson(m,lam):
	t = 0
	ilam = 1.0/lam
	for i in range(m):
		t += np.random.exponential(ilam)
	return t

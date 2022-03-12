import numpy as np
import matplotlib.pyplot as plt

class Vector:
    def __init__(self, x, y, normalized=False):
        if normalized:
            norm = np.sqrt(x**2 + y**2)
        else:
            norm = 1
        self.x = x / norm
        self.y = y / norm

    def turn(self):
        return Vector(-self.x, -self.y)

    def to_tuple(self):
        return (self.x, self.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) and len(other) == 2:
            return Vector(self.x + other[0], self.y + other[1])

class NacaProfile():
    def __init__(self, label, n, scale=1.0):
        self.set_parameters(label)
        self.x = np.linspace(0, 1, n) * scale
        self.yc = np.zeros(n)
        self.yt = np.zeros(n)
        self.slope = np.zeros(n)
        self.points = np.empty(shape=(n,4), dtype=np.float64)

    def set_parameters(self, number):
        number = str(number)
        self.M = int(number[0])/100
        self.P = int(number[1])/10
        self.T = int(number[2:])/100

    def calculate_camber(self):
        x1 = self.x[self.x <= self.P]
        x2 = self.x[self.x > self.P]

        a0 = 0.2969
        a1 = -0.126
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1036

        self.yc[:len(x1)] = self.M/self.P**2 * (2*self.P*x1 - x1**2)
        self.yc[len(x1):] = self.M/(1-self.P)**2 * (1 - 2*self.P +2*self.P*x2 - x2**2)

        self.yt = self.T / 0.2 * (a0*self.x**0.5 + a1*self.x + a2*self.x**2 + a3*self.x**3 + a4*self.x**4)

        self.slope[:len(x1)] = 2*self.M/self.P**2 * (self.P - x1)
        self.slope[len(x1):] = 2*self.M / (1 - self.P)**2 * (self.P - x2)

    def calculate_profile(self):
        for i in range(len(self.yc)):
            dir_vect = Vector(-self.slope[i], 1)
            self.points[i,0], self.points[i,1] =  (dir_vect*self.yt[i] + (self.x[i], self.yc[i])).to_tuple()
            self.points[i,2], self.points[i,3] = (dir_vect.turn()*self.yt[i] + (self.x[i], self.yc[i])).to_tuple()
        

    def disp(self):
        plt.plot(self.x, self.yc)
        plt.plot(self.points[:,0], self.points[:,1])
        plt.plot(self.points[:,2], self.points[:,3])
        plt.axis('equal')
        plt.grid(True, color='#d9d9d9', linestyle='--')
        plt.show()

p = NacaProfile('6412', 1000)
p.calculate_camber()
p.calculate_profile()
p.disp()
# print(p.points)
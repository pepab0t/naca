import numpy as np
import matplotlib.pyplot as plt

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)

class NacaProfile():
    def __init__(self, label, n, scale=1.0):
        self.set_parameters(label)
        self.x = np.linspace(0, 1, n) * scale
        self.yc = np.zeros(n)
        self.yt = np.zeros(n)
        self.slope = np.zeros(n)
        self.points = np.zeros(n)

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

    # def calculate_profile(self):
        

    def disp(self):
        print(self.yc)
        plt.plot(self.x, self.yc)
        plt.axis('equal')
        plt.grid(True, color='#d9d9d9', linestyle='--')
        plt.show()

p = NacaProfile(2412, 100)

p.calculate_camber()
p.disp()
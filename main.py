import numpy as np
import matplotlib.pyplot as plt

class NacaProfile():
    def __init__(self, label, n, scale=1.0):
        self.set_parameters(label)
        self.x = np.linspace(0, 1, n) * scale
        self.yc = np.zeros(n)

    def set_parameters(self, number):
        number = str(number)
        self.M = int(number[0])/100
        self.P = int(number[1])/10
        self.XX = int(number[2:])/100

    def calculate_camber(self):
        x1 = self.x[self.x <= self.P]
        x2 = self.x[self.x > self.P]

        self.yc[:len(x1)] = self.M/self.P**2 * (2*self.P*x1 - x1**2)
        self.yc[len(x1):] = self.M/(1-self.P**2) * (1 - 2*self.P +2*self.P*x2 - x2**2)

    def disp(self):
        print(self.yc)
        plt.plot(self.x, self.yc)
        plt.show()

p = NacaProfile(2412, 100)

p.calculate_camber()
p.disp()
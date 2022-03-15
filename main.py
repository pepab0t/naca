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
        elif isinstance(other, tuple) and len(other) == 2 and all([isinstance(x,float) for x in other]):
            return Vector(self.x + other[0], self.y + other[1])

class NacaProfile():
    def __init__(self, label, n, scale=1.0, area=[(-5, 5), (7, 5), (7, -5), (-5, -5)]):
        self.set_parameters(label)
        self.name = str(label)
        self.x = np.linspace(0, 1, n) * scale
        self.yc = np.zeros(n)
        self.yt = np.zeros(n)
        self.slope = np.zeros(n)
        self.points = np.empty(shape=(n,4), dtype=np.float64)
        self.area = area

    def set_parameters(self, number):
        number = str(number)
        self.M = int(number[0])/100
        self.P = int(number[1])/10
        self.T = int(number[2:])/100

        if self.M == 0:
            self.P == 0

    def calculate_camber(self):
        x1 = self.x[self.x <= self.P]
        x2 = self.x[self.x > self.P]

        a0 = 0.2969
        a1 = -0.126
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1036

        if self.P != 0:
            self.yc[:len(x1)] = self.M/self.P**2 * (2*self.P*x1 - x1**2)
            self.yc[len(x1):] = self.M/(1-self.P)**2 * (1 - 2*self.P +2*self.P*x2 - x2**2)

            self.slope[:len(x1)] = 2*self.M/self.P**2 * (self.P - x1)
            self.slope[len(x1):] = 2*self.M / (1 - self.P)**2 * (self.P - x2)
        else:
            self.yc[:] = 0
            self.slope[:] = 0

        self.yt = self.T / 0.2 * (a0*self.x**0.5 + a1*self.x + a2*self.x**2 + a3*self.x**3 + a4*self.x**4)

    def calculate_profile(self):
        if all(self.yc == 0):
            self.calculate_camber()
        for i in range(len(self.yc)):
            dir_vect = Vector(-self.slope[i], 1)
            self.points[i,0], self.points[i,1] =  (dir_vect*self.yt[i] + (self.x[i], self.yc[i])).to_tuple()
            self.points[i,2], self.points[i,3] = (dir_vect.turn()*self.yt[i] + (self.x[i], self.yc[i])).to_tuple()
        
        self.points[abs(self.points) < 1e-14] = 0

    def to_geo(self):
        point_counter = 0
        line_counter = 0
        k_point = 2
        with open(f'NACA_{self.name}.geo', 'w+') as f:
            f.write('//+\n')
            f.write(f'Point({1}) = ' + '{' + f'{self.points[0,0]}, {self.points[0,1]}, 0, 1.0' + '};\n')
            point_counter += 1
            for row in self.points[1:]:
                f.write('//+\n')
                f.write(f'Point({k_point}) = ' + '{' + f'{row[0]}, {row[1]}, 0, 1.0' + '};\n')
                f.write('//+\n')
                f.write(f'Point({k_point+len(self.points)}) = ' + '{' + f'{row[2]}, {row[3]}, 0, 1.0' + '};\n')
                k_point += 1
                point_counter += 2

            for p in self.area:
                f.write('//+\n')
                f.write(f'Point({k_point + len(self.points)}) = ' + '{' + f'{p[0]}, {p[1]}, 0, 1.0' + '};\n')
                k_point += 1

            f.write('//+\n')
            f.write(f'Line({1}) = ' + '{' + f'{1}, {2}' + '};\n')
            f.write('//+\n')
            f.write(f'Line({len(self.points)}) = ' + '{' + f'{1}, {2+len(self.points)}' + '};\n')

            for k_line in range(2, len(self.points)):
                f.write('//+\n')
                f.write(f'Line({k_line}) = ' + '{' + f'{k_line}, {k_line+1}' + '};\n')
                f.write('//+\n')
                f.write(f'Line({k_line-1+len(self.points)}) = ' + '{' + f'{k_line+len(self.points)}, {k_line+1+len(self.points)}' + '};\n')

            for i in range(len(self.area)):
                f.write('//+\n')
                if i == len(self.area)-1:
                    f.write(f'Line({i+1 + 2*(len(self.points)-1)}) = ' + '{' + f'{point_counter+i+2}, {point_counter+2}' + '};\n')
                else:
                    f.write(f'Line({i+1 + 2*(len(self.points)-1)}) = ' + '{' + f'{point_counter+i+2}, {point_counter+i+3}' + '};\n')

    def disp(self):
        plt.plot(self.x, self.yc, color='black', ls='--', lw=1)
        plt.plot(self.points[:,0], self.points[:,1], color='black', ls='-', lw=2)
        plt.plot(self.points[:,2], self.points[:,3], color='black', ls='-', lw=2)
        plt.axis('equal')
        plt.grid(True, color='#d9d9d9', linestyle='--')
        plt.show()

p = NacaProfile('6424', 100, area=[(-2, 2), (3, 2), (3, -2), (-2, -2)])
p.calculate_profile()
# p.disp()
p.to_geo()
# print(p.points)
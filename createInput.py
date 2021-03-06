from NacaGenerator import NacaProfile
from MakePoints import PointMaker
from entities import Line, Vector
from cython_stuff import shortest_distance_cy
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import time
import concurrent.futures



class DistField:

    def __init__(self, profile: NacaProfile, point_field: np.ndarray):
        """point_field needs to be in shape (n1,n2,2)"""

        self.naca = profile
        self.point_field = point_field.reshape(point_field.shape[0] * point_field.shape[1], point_field.shape[2])
        # self.X = np.array(np.meshgrid(point_field[:,0], point_field[:,1]))
        # print(self.X)
        # print(self.X.shape)

    def evaluate(self):

        distances = np.zeros(len(self.point_field))
        for i in range(len(self.point_field)):
            # distances[i] = self.shortest_distance(self.point_field[i,:])
            distances[i] = shortest_distance_cy(self.naca.upper, self.naca.lower, self.point_field[i,:])

        out = np.zeros(shape=(self.point_field.shape[0], self.point_field.shape[1]+1))
        out[:,0:2] = self.point_field#.copy()
        out[:,2] = distances

        return out

    def evaluate_parallel(self):

        with concurrent.futures.ProcessPoolExecutor() as executor:
            procs = [executor.submit(self.shortest_distance, point) for point in self.point_field]

        out = np.zeros(shape=(self.point_field.shape[0], self.point_field.shape[1]+1))
        out[:,0:2] = self.point_field.copy()
        
        for i in range(len(procs)):
            out[i,2] = procs[i].result()
            
        return out

    def evaluate_parallel_cy(self):

        with concurrent.futures.ProcessPoolExecutor() as executor:
            procs = [executor.submit(shortest_distance_cy, self.naca.upper, self.naca.lower, point) for point in self.point_field]

        out = np.zeros(shape=(self.point_field.shape[0], self.point_field.shape[1]+1))
        out[:,0:2] = self.point_field.copy()
        
        for i in range(len(procs)):
            out[i,2] = procs[i].result()
            
        return out

    def shortest_distance(self, point: np.ndarray) -> float:
        Line._validate_entity(point)

        d = 1e6

        for i in range(1, len(self.naca.upper)):
            l = Line(self.naca.upper[i-1,:], self.naca.upper[i,:])
            d_new = l.distance_segment(point)
            if d_new < d:
                d = d_new 

        for i in range(1, len(self.naca.lower)):
            l = Line(self.naca.lower[i-1,:], self.naca.lower[i,:])
            d_new = l.distance_segment(point)
            if d_new < d:
                d = d_new

        # IS OUTSIDE
        d = (-1) * int(self.naca.is_outside(point)) * d

        return d

def plot_data(xyz: np.ndarray, show:bool=True):
    x, y = xyz[:,0].copy(), xyz[:,1].copy()
    X, Y = np.meshgrid(xyz[:,0], xyz[:,1])

    Z = griddata((x, y), xyz[:,2], (X, Y), method='nearest')
    plt.contourf(X, Y, Z, 100)
    if show:
        plt.show()

def main():
    naca = NacaProfile('6424', 100)
    naca.calculate_profile()
    naca.transform_points(20)

    points = PointMaker(1.5, -1.5, -1.5, 1.5, 64,64).make()

    dist_field = DistField(naca, points)

    ## SEquential
    # tic = time.perf_counter()
    # p1 = dist_field.evaluate()
    # toc = time.perf_counter()
    # print(toc-tic)

    tic = time.perf_counter()
    p2 = dist_field.evaluate_parallel()
    toc = time.perf_counter()
    print(toc-tic)

    # tic = time.perf_counter()
    # p3 = dist_field.evaluate_parallel_cy()
    # toc = time.perf_counter()
    # print(toc-tic)

    # print((p2==p3).all())

    plot_data(p2, show=True)
    # naca.disp(camber=False, show=False)
    # points.display(points.make(), show=True)

if __name__ == '__main__':
    main()
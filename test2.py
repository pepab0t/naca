import numpy as np
from createInput import Vector

v1 = np.array([2,0])

v = np.array([1,1])

phi = 45 * np.pi / 180
l = 1

u = np.ones(2)

u[0] = np.cos(phi) * v1[0] - np.sin(phi) * v1[1]
u[1] = np.sin(phi) * v1[0] + np.cos(phi) * v1[1]

# print(np.round(u,0))

print(Vector.angle(u, v))


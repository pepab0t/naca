from ipaddress import summarize_address_range
import numpy
from pandas import concat
cimport numpy

from entities import Line, Vector

ctypedef numpy.float_t DTYPE_t

def outside_check(numpy.ndarray[DTYPE_t, ndim=2] upper, numpy.ndarray[DTYPE_t, ndim=2] lower, numpy.ndarray[DTYPE_t, ndim=1] point):
    Line._validate_entity(point)

    cdef double sum_angle = 0
    cdef numpy.ndarray profile_points
    cdef int i
    cdef double alpha

    profile_points = numpy.concatenate([upper[::-1], lower])

    for i in range(1,len(profile_points)):
        a = profile_points[i-1, :] - point
        b = profile_points[i, :] - point
        # print(profile_points[i-1, :], profile_points[i, :])
        alpha = numpy.arcsin( Vector.vector_mul(a, b) / (Vector.magnitude(a) * Vector.magnitude(b))) * 180/numpy.pi
        # print(alpha)
        # self.disp(camber=False, show=False)
        # plt.plot([point[0], point[0]+a[0]], [point[1], point[1]+a[1]], 'r')
        # plt.plot([point[0], point[0]+b[0]], [point[1], point[1]+b[1]], 'b')
        # plt.show()
        sum_angle += alpha

    return sum_angle < 180

def outside_check_py(upper, lower, point):
    Line._validate_entity(point)
    profile_points = numpy.concatenate([upper[::-1], lower])
    sum_angle = 0

    for i in range(1,len(profile_points)):
        a = profile_points[i-1, :] - point
        b = profile_points[i, :] - point
        # print(profile_points[i-1, :], profile_points[i, :])
        alpha = numpy.arcsin( Vector.vector_mul(a, b) / (Vector.magnitude(a) * Vector.magnitude(b))) * 180/numpy.pi
        # print(alpha)
        # self.disp(camber=False, show=False)
        # plt.plot([point[0], point[0]+a[0]], [point[1], point[1]+a[1]], 'r')
        # plt.plot([point[0], point[0]+b[0]], [point[1], point[1]+b[1]], 'b')
        # plt.show()
        sum_angle += alpha

    return sum_angle < 180

def shortest_distance_cy(numpy.ndarray[DTYPE_t, ndim=2] upper, numpy.ndarray[DTYPE_t, ndim=2] lower, numpy.ndarray[DTYPE_t, ndim=1] point):
    Line._validate_entity(point)
    cdef int i
    cdef double d = 1e6
    cdef double d_new

    for i in range(1, len(upper)):
        l = Line(upper[i-1,:], upper[i,:])
        d_new = l.distance_segment(point)
        if d_new < d:
            d = d_new 

    for i in range(1, len(lower)):
        l = Line(lower[i-1,:], lower[i,:])
        d_new = l.distance_segment(point)
        if d_new < d:
            d = d_new

    # IS OUTSIDE
    d = (-1) * int(outside_check(upper, lower, point)) * d

    return d

def shortest_distance_py(upper: numpy.ndarray, lower: numpy.ndarray, point: numpy.ndarray) -> float:
        Line._validate_entity(point)

        d = 1e6

        for i in range(1, len(upper)):
            l = Line(upper[i-1,:], upper[i,:])
            d_new = l.distance_segment(point)
            if d_new < d:
                d = d_new 

        for i in range(1, len(lower)):
            l = Line(lower[i-1,:], lower[i,:])
            d_new = l.distance_segment(point)
            if d_new < d:
                d = d_new

        # IS OUTSIDE
        d = (-1) * int(outside_check_py(upper, lower, point)) * d

        return d
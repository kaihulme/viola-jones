import math
import cv2 as cv
import numpy as np
from darts.manipulation.convolution import Convolution, convolution
from darts.manipulation.utils import threshold

from scipy.signal import convolve2d

class Sobel():
    def __init__(self):
        self.dfdx = []
        self.dfdy = []
        self.magnitude = []
        self.direction = []
        self.t_magnitude = []
        self._r_i = 1
        self._r_j = 1
        self._dfdx_kernel = [[-1, 0, 1],
                             [-1, 0, 1],
                             [-1, 0, 1]]
        self._dfdy_kernel = [[-1,-1,-1],
                             [ 0, 0, 0],
                             [ 1, 1, 1]]

    def edgedetection(self, frame, threshold_val):
        """
        Apply sobel edge detection to frame
        """
        rows, cols = frame.shape        
        self.dfdx = convolve2d(frame, self._dfdx_kernel, boundary='symm', mode='same') # faster than my implementation
        self.dfdy = convolve2d(frame, self._dfdy_kernel, boundary='symm', mode='same')
        # self.dfdx = Convolution(frame, self._dfdx_kernel, self._r_i, self._r_j).convolveframe()
        # self.dfdy = Convolution(frame, self._dfdy_kernel, self._r_i, self._r_j).convolveframe()
        # self.dfdx = convolution(frame, self._dfdx_kernel, self._r_i, self._r_j)
        # self.dfdy = convolution(frame, self._dfdy_kernel, self._r_i, self._r_j)
        self.magnitude = np.zeros((rows, cols), dtype=float)
        self.direction = np.zeros((rows, cols), dtype=float)
        # magnitude: ∇|f(x,y)| = sqrt( (df/dx)^2 + (df/dy)^2 )
	    # direction: φ = arctan( (df/dy) / (df/dx) )
        for y in range(rows):
            for x in range(cols):
                dfdx_val = self.dfdx[y][x]
                dfdy_val = self.dfdy[y][x]
                self.magnitude[y][x] = math.sqrt((dfdx_val**2) + (dfdy_val**2))
                self.direction[y][x] = math.atan2(dfdy_val, dfdx_val)
        self.t_magnitude = threshold(self.magnitude, threshold_val)
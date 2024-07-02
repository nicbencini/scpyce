"""
Contains the object classes for point load objects of the structural model.
"""

import numpy as np
from objects import element # pylint: disable=import-error

class PointLoad:
    """
    Creates a point load object from a node defining the location and the 6 degrees
    of freedom representing the load applications.
    """
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self,
                 node : element.Node,
                 fx : float,
                 fy : float,
                 fz : float,
                 mx : float,
                 my : float,
                 mz : float
                 ):

        self.node = node
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz

    def to_string(self):
        """Returns a string representing the object."""

        return f'Load ({self.fx},{self.fy},{self.fz},{self.mx},{self.my},{self.mz})'

    def to_array(self):
        """Returns an array with the object variables."""

        return np.array([self.fx,
                         self.fy,
                         self.fz,
                         self.mx,
                         self.my,
                         self.mz])

"""
Contains the object classes for element objects of the structural model.
"""
import uuid
import numpy as np

from geometry import vector_3d # pylint: disable=import-error
from geometry import plane # pylint: disable=import-error
from objects import properties # pylint: disable=import-error

class Node:
    """
    Node object that represents a point in 3d space. 

    Parameters:
    x (float): The x coordinate of the node.
    y (float): The y coordinate of the node.
    z (float): The z coordinate of the node.

    Returns:
    Node object: Node object at the specified location.
    """

    def __init__(self,
                 x : float,
                 y : float,
                 z : float):

        self.x = x
        self.y = y
        self.z = z


    def to_string(self):
        """
        Returns a string representing the object.
        
        Parameters:
        None

        Returns:
        string: String representing the node object.
        """

        return f'Node at ({self.x},{self.y},{self.z})'

    def to_array(self):
        """
        Returns an array with the object variables.
        
        Parameters:
        None

        Returns:
        numpy array: Array representing the node object.
        """

        return np.array([self.x,self.y,self.z])


class Bar:
    """
    Bar object that represents a line between two nodes and contains stiffness
    and end release information for the element.

    Bar elements may be given a custom name for reference however if no name is
    given the bar will be assigned a guid. Bar names must be unique otherwise 
    bars with confilicting names will be overwritted once added to the database
    model.

    Parameters:
    node_a (node object): Node representing the start point of the bar.
    node_b (node object): Node representing the end point of the bar.
    section (section object): Section property for bar.
    orientation_vector (vector): Vector representing orientation of bar.
    release_a (string): String representing releases of bar start node.
    release_b (string): String representing releases of bar end node.
    name (string): The name of the bar.

    Returns:
    bar objcet: The created bar object.
    """

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self,
                 node_a : Node,
                 node_b : Node,
                 section : properties.Section,
                 orientation_vector : np.array,
                 release_a : str = 'XXXXXX',
                 release_b : str = 'XXXXXX',
                 name : str = None
                 ):

        # pylint: disable=too-many-arguments
        # Eight is reasonable in this case.

        self.node_a = node_a
        self.node_b = node_b
        self.section = section
        self.orientation_vector = orientation_vector
        self.release_a = release_a
        self.release_b = release_b
        self.name = name if name is not None else str(uuid.uuid4())
        self.length = vector_3d.length(node_a.to_array(),node_b.to_array())


    def local_stiffness_matrix(self):
        """
        Builds the local stiffness matrix for the bar based on the geometrical and structural
        information for the bar.

        Parameters:
        None

        Returns:
        numpy array: Array representing the local stiffness matrix.
        """
        # pylint: disable=too-many-locals
        # Seven is reasonable in this case.

        #Fix units for E and G <--------

        A = self.section.area # pylint: disable=invalid-name
        E = self.section.material.youngs_modulus * 1000000 # pylint: disable=invalid-name
        Iz = self.section.izz # pylint: disable=invalid-name
        Iy = self.section.iyy # pylint: disable=invalid-name
        G =  self.section.material.shear_modulus * 1000000 # pylint: disable=invalid-name
        J =  Iz + Iy # pylint: disable=invalid-name
        L = self.length # pylint: disable=invalid-name

        # Axial coefficient

        a1 = E*A/L

        #Torsional coefficient
        t1 = G*J/L

        #Shear coeffiecient - Major Axis
        v1 = 12*E*Iz/L**3
        v2 = 6*E*Iz/L**2

        #Shear coeffiecient - Minor Axis
        v3 = 12*E*Iy/L**3
        v4 = 6*E*Iy/L**2

        #Moment coeffiecient - Major Axis
        m1 = 6*E*Iz/L**2
        m2 = 4*E*Iz/L
        m3 = 2*E*Iz/L

        #Moment coeffiecient - Minor Axis
        m4 = 6*E*Iy/L**2
        m5 = 4*E*Iy/L
        m6 = 2*E*Iy/L


        #Build local stiffness matrix
        kl = [[  a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
                [ 0.0 ,  v1 , 0.0 , 0.0 , 0.0 , -m1 , 0.0 , -v1 , 0.0 , 0.0 , 0.0 , -m1 ],
                [ 0.0 , 0.0 ,  v3 , 0.0 ,  m4 , 0.0 , 0.0 , 0.0 , -v3 , 0.0 ,  m4 , 0.0 ],
                [ 0.0 , 0.0 , 0.0 ,  t1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -t1 , 0.0 , 0.0 ],
                [ 0.0 , 0.0 ,  v4 , 0.0 ,  m5 , 0.0 , 0.0 , 0.0 , -v4 , 0.0 ,  m6 , 0.0 ],
                [ 0.0 , -v2 , 0.0 , 0.0 , 0.0 ,  m2 , 0.0 ,  v2 , 0.0 , 0.0 , 0.0 ,  m3 ],
                [ -a1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , a1  , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
                [ 0.0 , -v1 , 0.0 , 0.0 , 0.0 ,  m1 , 0.0 ,  v1 , 0.0 , 0.0 , 0.0 ,  m1 ],
                [ 0.0 , 0.0 , -v3 , 0.0 , -m4 , 0.0 , 0.0 , 0.0 ,  v3 , 0.0 , -m4 , 0.0 ],
                [ 0.0 , 0.0 , 0.0 , -t1 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,  t1 , 0.0 , 0.0 ],
                [ 0.0 , 0.0 ,  v4 , 0.0 ,  m6 , 0.0 , 0.0 , 0.0 , -v4 , 0.0 ,  m5 , 0.0 ],
                [ 0.0 , -v2 , 0.0 , 0.0 , 0.0 ,  m3 , 0.0 ,  v2 , 0.0 , 0.0 , 0.0 ,  m2 ],
                ]

        #Remove released coefficients

        combined_release_string = self.release_a + self.release_b

        count = 0

        for char in combined_release_string:

            if char == "F":

                divisor = kl[count,count]# pylint: disable=invalid-sequence-index

                row_values = np.divide(kl[count,:],divisor)# pylint: disable=invalid-sequence-index
                col_values = kl[:,count]# pylint: disable=invalid-sequence-index

                subtraction_vector = np.outer(col_values,row_values)

                kl = np.subtract(kl,subtraction_vector)


            count += 1

        return kl

    def transformation_matrix(self):
        """
        Builds the transformation matrix for the bar from local coordinates to global coordinates.

        
        Parameters:
        None

        Returns:
        numpy array: Array representing the local transformation matrix.
        """

        #Build the full transformation matrix for this element
        tm = np.zeros((12,12))

        local_plane = plane.plane_from_3pt(self.node_a.to_array(),
                                                       self.node_b.to_array(),
                                                       self.orientation_vector,
                                                       True
                                                       )

        t_repeat =  np.array([local_plane[1],
                            local_plane[2],
                            local_plane[3]]
                            )


        tm[0:3,0:3] = t_repeat
        tm[3:6,3:6] = t_repeat
        tm[6:9,6:9] = t_repeat
        tm[9:12,9:12] = t_repeat

        return tm


class Support:
    """
    Creates a 6 degeree of freedom node support object. Each degree of freedom is represented by a bool.
    True = fixed, False = released.

    Parameters:
    node (node object): The node location of the support.
    fx (bool): The fixity of translations in the x direction.
    fy (bool): The fixity of translations in the y direction.
    fz (bool): The fixity of translations in the z direction.
    mx (bool): The fixity of rotations about the x axis.
    my (bool): The fixity of rotations about the y axis.
    mz (bool): The fixity of rotations about the z axis.

    Returns:
    support object: The defined support object.
    """

    def __init__(self,
                 node : Node,
                 fx : bool,
                 fy : bool,
                 fz : bool,
                 mx : bool,
                 my : bool,
                 mz : bool
                 ):

        # pylint: disable=too-many-arguments
        # Seven is reasonable in this case.

        self.node = node
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz

    def set_fix(self):
        """
        Sets the support to fully fixed.

        Parameters:
        None

        Returns:
        support object: Fully fixed support object.
        """
        self.fx = True
        self.fy = True
        self.fz = True
        self.mx = True
        self.my = True
        self.mz = True

    def set_pin(self):
        """
        Sets the support to pinned with rotoational releases only.

        Parameters:
        None

        Returns:
        support object: Pinned support object.
        """
        self.fx = True
        self.fy = True
        self.fz = True
        self.mx = False
        self.my = False
        self.mz = False

    @staticmethod

    def pin(node):
        # pylint: disable=no-self-argument
        """
        Returns a pinned support at the given node location.
        
        Parameters:
        None

        Returns:
        support object: Pinned support object.
        """

        return Support(node,True,True,True,False,False,False)

    def fix(node):
        # pylint: disable=no-self-argument
        """
        Returns a fixed support at the given node location.
        
        Parameters:
        None
        
        Returns:
        support object: Pinned support object.
        """

        return Support(node,True,True,True,True,True,True)

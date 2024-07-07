"""
Contains the Model class for building and modifying the structural SQLite database 
model which contains the geometrical and structural data used by the solver. 

Results from the solver are stored in the model database after the solver is run.

This module references the tables.py, read.py and write.py modules for reading and 
modifying the database model.

"""

import sqlite3

from model import tables # pylint: disable=import-error
from model import write # pylint: disable=import-error
from model import read # pylint: disable=import-error

class Model:
    """
    Used for creating the tables for the database model and 
    reading and writing into the databse. 

    The Model class contains the variable for the file path to the model
    and the SQLite connection.

    IMPORTANT: 
    - The build_tables method must be run to create the model tables before
    data is stored in the model. 
    -The close_connection method must be run to end work
    on the model and close the connection to the SQLite database.
    """
    def __init__(self , file_path):
        self.database_path = file_path
        self.connection = sqlite3.connect(self.database_path)

        print(f'Connected to {self.database_path}')

    def build_tables(self):
        """
        Creates the following tables for the SQLite database model: 

        - nodes
        - bars
        - sections
        - materials
        - supports
        - loads
        - node reactions
        - node displacements

        Parameters:
        None

        Returns:
        None
        """

        #Build object tables
        tables.build_bar_table(self.connection)
        tables.build_node_table(self.connection)
        tables.build_support_table(self.connection)

        #Build property tables
        tables.build_material_table(self.connection)
        tables.build_section_table(self.connection)

        #Build load tables
        tables.build_point_load_table(self.connection)

        #Build results tables
        tables.build_node_displacements_table(self.connection)
        tables.build_node_reactions_table(self.connection)

    def add_bar(self, bar): # pylint: disable=disallowed-name
        """
        Adds a bar to the database. Returns the id of that bar. 
        If the bar already exists it will return the id of the existing bar.

        Parameters:
        bar (bar object): The bar object to add to the database

        Returns:
        None
        """
        write.add_bar(self, bar)

    def add_node(self, node):
        """
        Adds a node to the database.
        
        Parameters:
        node (node object): The node object to add to the database.

        Returns:
        None
        """

        write.add_node(self, node)


    def add_material(self, material):
        """
        Adds a material to the database.
        
        Parameters:
        material (material object): The material object to add to the database.

        Returns:
        None
        """

        write.add_material(self, material)

    def add_section(self, section):
        """
        Adds a section to the database.
        
        Parameters:
        section (section object): The section object to add to the database.

        Returns:
        None
        """

        write.add_section(self,section)

    def add_support(self, support):
        """
        Adds a support to the database.
        
        Parameters:
        support (support object): The support object to add to the database.

        Returns:
        None
        """
    

        write.add_support(self, support)

    def add_point_load(self, pointload):
        """
        Adds a point load to the database.
        
        Parameters:
        pointload (pointload object): The pointload object to add to the database.

        Returns:
        None
        """

        write.add_point_load(self, pointload)

    def get_material(self, material_name):
        """
        Gets a material from the database using the material name as reference.
        
        Parameters:
        material_name (string): The name of the material to retreive from the database.

        Returns:
        material object: The retreived material. 
        """

        material_object = read.get_material(self, material_name)

        return material_object

    def get_section(self, section_name):
        """
        Gets a section from the database using the section name as reference.
        
        Parameters:
        section_name (string): The name of the section to retreive from the database.

        Returns:
        section object: The retreived section.
        """

        section_object = read.get_section(self, section_name)

        return section_object

    def get_node(self, node_index):
        """
        Gets a node from the database using the node index as a reference.
        
        Parameters:
        node_index (float): The index of the node to retreive from the database.

        Returns:
        node object: The retreived node.
        """

        node_object = read.get_node(self, node_index)

        return node_object

    def get_bar(self, bar_name):
        """
        Gets a bar from the database using the bar name as a reference.

        Parameters:
        bar_name (string): The name of the bar to retreive from the database.

        Returns:
        bar object: The retreived bar.        
        """

        bar_object = read.get_bar(self, bar_name)

        return bar_object


    def close_connection(self):
        """
        Closes the connection to the model database.
        
        Parameters:
        None

        Returns:
        None        
        """

        self.connection.close()
        print( f'Connection to {self.database_path} closed')

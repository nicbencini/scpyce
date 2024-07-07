"""
Contains functions for reading information from the SQLite database model.
"""
import sqlite3
import numpy as np

from objects import properties # pylint: disable=import-error
from objects import element # pylint: disable=import-error

def get_material(database, material_name):
    """ 
    Gets a material object from the SQLite database tables based on a material name reference.

    Parameters:
    material_name (string): The name of the material to retreive from the database.

    Returns:
    material object: The retreived material. 
    """

    material_cursor = database.connection.cursor()
    material_data = material_cursor.execute("SELECT * FROM property_material WHERE _id = ?",[material_name]).fetchone()
    material_object = properties.Material(*material_data)
    material_cursor.close()

    return material_object

def get_section(database, section_name):
    """ 
    Gets a section object from the SQLite database tables based on a section name reference.

    Parameters:
    section_name (string): The name of the section to retreive from the database.

    Returns:
    section object: The retreived section. 
    """

    section_cursor = database.connection.cursor()
    section_data = section_cursor.execute("SELECT * FROM property_section WHERE _id = ?",[section_name]).fetchone()
    section_data = list(section_data)
    section_data[1] = get_material(database, section_data[1])
    section_object = properties.Section(*section_data)
    section_cursor.close()

    return section_object

def get_node(database, node_index):
    """ 
    Gets a node object from the SQLite database tables based on a node index reference.

    Parameters:
    node_index (float): The index of the node to retreive from the database.

    Returns:
    node object: The retreived node.
    """

    node_cursor = database.connection.cursor()
    node_data = node_cursor.execute("SELECT * FROM element_node LIMIT 1 OFFSET ?",[int(node_index)]).fetchone()

    node_object = element.Node(node_data[1],
                                node_data[2],
                                node_data[3])

    node_cursor.close()

    return node_object

def get_bar(database, bar_name):
    """ 
    Gets a bar object from the SQLite database tables based on a bar name reference.

    Parameters:
    bar_name (string): The name of the bar to retreive from the database.

    Returns:
    bar object: The retreived bar.  
    """

    bar_cursor = database.connection.cursor()
    bar_data = bar_cursor.execute("SELECT * FROM element_bar WHERE _id = ?",[bar_name]).fetchone()
    bar_data = list(bar_data)

    id = bar_data[0]
    node_a = get_node(database, bar_data[1])
    node_b = get_node(database, bar_data[2])
    section = get_section(database, bar_data[3])

    orientation_vector = str.replace(bar_data[4],'[','')
    orientation_vector = str.replace(orientation_vector,']','')
    orientation_vector = str.split(orientation_vector,' ')

    orientation_vector = np.array([float(orientation_vector[0]),
                                    float(orientation_vector[1]),
                                    float(orientation_vector[2])]
                                    )

    release_a = bar_data[5]
    release_b = bar_data[6]

    bar_object = element.Bar(node_a,
                                node_b,
                                section,
                                orientation_vector,
                                release_a,
                                release_b,
                                id)

    return bar_object

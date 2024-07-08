"""
Example for building and solving a pyramid structure.
"""

import os
import numpy as np

from context import database # pylint: disable=import-error
from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error
from context import lind_solver # pylint: disable=import-error

# Define database model path
db_path = os.path.dirname(os.path.realpath(__file__)) + '/pyramid_example.db'

# Define nodes
node1 = element.Node(0.5,0.5,1)
node2 = element.Node(1,0,0)
node3 = element.Node(0,0,0)
node4 = element.Node(1,1,0)
node5 = element.Node(0,1,0)

# Define section properties
section = properties.Section.default()
orientation_vector = np.array([1,0,0])

# Define bars
bar1 = element.Bar(node1,node2,section,orientation_vector)
bar2 = element.Bar(node1,node3,section,orientation_vector)
bar3 = element.Bar(node1,node4,section,orientation_vector)
bar4 = element.Bar(node1,node5,section,orientation_vector)

# Define supports
support1 = element.Support.pin(node2)
support2 = element.Support.pin(node3)
support3 = element.Support.pin(node4)
support4 = element.Support.pin(node5)

# Define loads
load1 = load.PointLoad(node1,0,0,10,0,0,0)

# Create structural model
structural_model = database.Model(db_path)
structural_model.build_tables()

# Add bars
structural_model.add_bar(bar1)
structural_model.add_bar(bar2)
structural_model.add_bar(bar3)
structural_model.add_bar(bar4)

# Add supports
structural_model.add_support(support1)
structural_model.add_support(support2)
structural_model.add_support(support3)
structural_model.add_support(support4)

# Add loads
structural_model.add_point_load(load1)

# Run solver
lind_solver.solve(structural_model)

# Close model
structural_model.close_connection()

"""
Generates the documentation for the project.
"""

import pydoc
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/scpyce_solver/scpyce/'
sys.path.append(parent_dir)

path = parent_dir + 'geometry/plane.py'

print (path)

pydoc.writedocs(path)
"""
Generates the documentation for the project.
"""

import pydoc
import os
import sys
import shutil

source_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = source_dir + '/scpyce/'
sys.path.append(parent_dir)
sys.path.append(source_dir)


sourcefiles = os.listdir(source_dir)

pydoc.writedocs(source_dir)

for file in sourcefiles:
    if file.endswith('.html'):
        shutil.move(os.path.join(source_dir,file), os.path.join(source_dir + '/docs/',file))
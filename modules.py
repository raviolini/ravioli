"""
    Enables imports from `modules` folder
"""

import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'modules'))

import siakad_auto_attendance

del sys.path[0], sys, os

"""
    Enables imports from `pasta` folder
"""

import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'pasta'))

import siakad_auto_attendance #don't remove this unused import

del sys.path[0], sys, os

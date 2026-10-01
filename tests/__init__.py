# Needed to treat this folder as a module so tests will run.

import sys
try:
    import sympy as sp
except ModuleNotFoundError:
    print("SymPy is not installed.")
    sys.exit(1)
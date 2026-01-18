# When importing a module with
#    import myPackage
# Python will only bring the TOP-LEVEL package into the current namespace;
# NOT the entire package hierarchy. All the subpackages (i.e. the directories
# inside the package directory) and the modules (i.e. the .py files) WON'T be
# imported, therefore a statement like
#    z = myPackage.myModule1.myCode1.my_example_function_1(x)
# won't work because Python won't see any "myModule1" subpackage

# To fix the problem, you have 2 solutions:
# 1) EITHER import each MODULE separately
#	import myPackage.myModule1.myCode1 as myC1
#	z = myC1.my_example_function_1(x)
# 2) OR add some import statements into the __init__.py files, so that Python
# will do all the imports under the hood.
# In particular:
# a) import the SUBPACKAGES from withing the top-level
from . import meangen
from . import stagen
from . import multall
from . import plotutils
from . import auxiliaries
# b) and then import the MODULES from within each subpackage
# (see all the other __init__.py files in the subdirectories of this package)

__version__ = '1.0.1'
__author__ = ['Andrea Pinardi', 'John Denton']
__email__ = ['andrea.pinardi@polimi.it', 'jdd1@cam.ac.uk']
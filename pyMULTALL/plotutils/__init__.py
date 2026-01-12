# For the explaination of the these import statements, see the __init__.py
# file in the top-level directory of the package.
# In short: each __init__.py import the subpackages (i.e. the subdirectories
# contained in the parent directory of the __init__.py) in a "cascade", until
# yuo reach the lowest level where no more subpackages exist.
# At that level, import each module (i.e. the single .py files).
# In this way, you'll be able to import the entire package (with all its
# subpackages and modules promptly available) with just
#	import myPackage

#from . import myCode1

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Define module-level variables with version-related information
with open(os.path.join(dir_path, 'version.dat'), 'r') as _version:
    __version__ = _version.read()


# Function to retrieve the version
def version():
    """Returns the version of the module."""
    return __version__

# Import version-related information from the "_version" module
from ._version import _VERSION, _AUTHOR_EMAIL, _AUTHOR, _TITLE
from ._version import _MAINTAINER, _DESCRIPTION, _DOCS_URL, _PROJECT_URL

# Define module-level variables with version-related information
__version__ = _VERSION
__maintainer__ = _MAINTAINER
__author__ = _AUTHOR
__author_email__ = _AUTHOR_EMAIL
__description__ = _DESCRIPTION
__title__ = _TITLE
__project_url__ = _PROJECT_URL
__docs_url__ = _DOCS_URL

# Function to retrieve the version
def version():
    """Returns the version of the module."""
    return __version__

# Function to retrieve the title
def title():
    """Returns the title of the module."""
    return __title__

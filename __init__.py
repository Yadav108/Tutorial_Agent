"""
Tutorial Agent - An interactive programming learning platform
"""

__version__ = '2.0.0'
__author__ = 'Aryan Yadav'
__license__ = 'MIT'

from . import gui
from . import services
from . import utils
from . import database
from . import config

# Version information
VERSION_INFO = {
    'major': 1,
    'minor': 0,
    'patch': 0,
    'release': 'final'
}

# Setup logging
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
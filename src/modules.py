# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                      Charcoal Editor                      #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
    import sys
    import os
    import keyword
    import pkgutil
    import re
    import types
    import builtins
    from pathlib import Path
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.Qsci import *
    from PyQt5.QtGui import *
    from jedi import Script
    from jedi.api import Completion

except ImportError:
    raise ImportError("Charcoal couldn't import all of the necessary packages.")

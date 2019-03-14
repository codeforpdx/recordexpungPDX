from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect

debug_toolbar = DebugToolbarExtension()
csrf = CSRFProtect()
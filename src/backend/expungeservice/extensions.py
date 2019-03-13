from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CsrfProtect

debug_toolbar = DebugToolbarExtension()
csrf = CsrfProtect()
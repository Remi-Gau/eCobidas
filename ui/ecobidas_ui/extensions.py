"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bootstrap import Bootstrap5
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect

bootstrap = Bootstrap5()
csrf_protect = CSRFProtect()
cache = Cache()
debug_toolbar = DebugToolbarExtension()

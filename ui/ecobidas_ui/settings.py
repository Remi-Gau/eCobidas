from pathlib import Path

from environs import Env

env = Env()
env.read_env()

ROOT_DIR = Path(__file__).parent

# Static content
STATIC_FOLDER = ROOT_DIR / "static"

# Templates
TEMPLATE_FOLDER = ROOT_DIR / "templates"

UPLOAD_FOLDER = Path(__file__).parent / "tmp"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ---- SETUP INSTRUCTIONS AND APP BEHAVIOR ####

# ------ App-level configuration ###
DEBUG = True

PROTOTYPE = True

SECRET_KEY = env.str("SECRET_KEY")

# CACHE_TYPE = "flask_caching.backends.SimpleCache"  # Can be "MemcachedCache", "RedisCache", etc.

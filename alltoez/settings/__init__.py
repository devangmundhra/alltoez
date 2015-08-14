import os

from common.utils import get_env_variable

try:
   ENVIRONMENT = get_env_variable('ENVIRONMENT')
except Exception:
   ENVIRONMENT = "local"

if ENVIRONMENT == "production":
   from .production import *
elif ENVIRONMENT == "staging":
   from .dev import *
else:
   from .local import *

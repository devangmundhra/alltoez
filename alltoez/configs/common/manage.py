#!/usr/bin/env python

import os
import sys

# we want a few paths on the python path
# first up we add the root above the application so
# we can have absolute paths everywhere
python_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../../'
)
# we have have a local apps directory
apps_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../'
)


# we add them first to avoid any collisions
sys.path.insert(0, apps_path)
sys.path.insert(0, python_path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.common.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

from django.conf import settings
from subprocess import call
import os

def remove_duplicates(lst):
    new_lst = []
    
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)

    return new_lst


def reload_code():
    staging_file = os.path.join(settings.SITE_ROOT, 'configs/staging/staging.wsgi')
    production_file = os.path.join(settings.SITE_ROOT, 'configs/production/production.wsgi')
    
    call(['touch', staging_file])
    call(['touch', production_file])

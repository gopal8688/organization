import os

from django import template
#from django.contrib.sites.shortcuts import get_current_site

register = template.Library()

@register.simple_tag(name='script_includer')
def ifFileExists(filepath):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(BASE_DIR, 'static') #, 'scripts', "%s.js"%filepath)
    #print ('path',filepath1, get_current_site())
    print ('----',filepath)
    if os.path.exists(filepath):
        #return '<script src="%s"></script>'%filepath
        return True
    else:
        return False
import re
import sys, os
import jinja2
import markdown
from pykwiki.core import conf, ctrl

def idsafe(value):
    return re.sub(r'[^a-zA-Z0-9_\-]','_', value)



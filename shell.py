#!/usr/bin/env python

import IPython

from app import *

welcome_message = """
Stratigy Flask Shell
====================

The following variables are available to use:

app -> Stratigy Flask app instance.
"""

IPython.embed(header=welcome_message)

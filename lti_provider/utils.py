
# Copyright (c) 2018 Josef Wachtler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module provides some helper functions for the LTI Provider.
"""

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured


def get_by_py_path(py_path):
    """
    Imports and returns a python callable.

    Keyword arguments:
        py_path -- callable to load
    """
    parts = py_path.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def reverse_from_settings(parameter_to_view):
    """
    takes a tuple where the first element is the name of a view and the
    optional second parameter is a tuple, a list or a dictonary of the
    parameters for the view.

    keyword arguments:
        - parameter_to_view -- tuple of parameters
    """
    l = len(parameter_to_view)
    if l == 1:
        return reverse(parameter_to_view[0])
    elif l == 2:
        return reverse(parameter_to_view[0], args=parameter_to_view[1])
    else:
        raise ImproperlyConfigured('too much parameters')

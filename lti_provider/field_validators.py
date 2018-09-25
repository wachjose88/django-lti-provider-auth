
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
This module provides validators for model fields of the lti_provider-App.
"""

import logging
from oauthlib.oauth1.rfc5849.utils import UNICODE_ASCII_CHARACTER_SET

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Get an instance of a logger
logger = logging.getLogger('LTI.lti_provider')


def validate_oauth_chars(value):
    """
    Validates if there are only unicode ascii characters.

    Keyword arguments:
        - value -- string to validate
    """
    a = set(UNICODE_ASCII_CHARACTER_SET)
    v = set(value)
    if not v <= a:
        logger.debug('unsave characters')
        raise ValidationError(
            _('%(value)s contains unsave characters.'),
            params={'value': value},
        )


def validate_oauth_length(value):
    """
    Validates if the length is between 20 and 30.

    Keyword arguments:
        - value -- string to validate
    """
    length = len(value)
    if length > 30:
        logger.debug('too long')
        raise ValidationError(
            _('%(value)s characters are too much. Max length: 30'),
            params={'value': str(length)},
        )
    if length < 20:
        logger.debug('too short')
        raise ValidationError(
            _('%(value)s characters are too few. Min length: 20'),
            params={'value': str(length)},
        )

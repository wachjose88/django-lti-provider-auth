
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
This module provides all Django-Database-Models of the lti_provider-App.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from lti_provider.field_validators import validate_oauth_chars, \
                                          validate_oauth_length


class Consumer(models.Model):
    """
    This model saves information about the consumers.

    Fields:
        - key -- a key to identify a consumer
        - secret -- the key of the consumer
        - user -- a user responsible for a consumer
    """
    key = models.CharField(max_length=128, unique=True,
                           verbose_name=_('Key'),
                           validators=[validate_oauth_chars,
                                       validate_oauth_length])
    secret = models.CharField(max_length=128, unique=True,
                              verbose_name=_('Secret'),
                              validators=[validate_oauth_chars,
                                          validate_oauth_length])
    user = models.ForeignKey(User, verbose_name=_('User'))

    def __str__(self):
        """
        unicode representation
        """
        return str(self.key)

    class Meta:
        verbose_name = _('Consumer')
        verbose_name_plural = _('Consumers')


class TimestampAndNonce(models.Model):
    """
    This model stores the timestamp and its related nonce of a request
    from a consumer.

    Fields:
        - consumer -- the consumer of the request
        - timestamp -- time of the request as int
        - nonce -- a string related to this timestamp only
    """
    consumer = models.ForeignKey(Consumer, verbose_name=_('Consumer'))

    timestamp = models.IntegerField(verbose_name=_('Timestamp'))
    nonce = models.CharField(max_length=128, verbose_name=_('Nonce'))

    def __str__(self):
        """
        unicode representation
        """
        return str(self.timestamp)

    class Meta:
        unique_together = ('timestamp', 'nonce')
        verbose_name = _('Timestamp and Nonce')
        verbose_name_plural = _('Timestamps and Nonces')

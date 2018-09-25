
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
This module provides validators for the LTI request of the lti_provider-App.
"""

import logging
from oauthlib.oauth1 import RequestValidator
from lti_provider.models import Consumer, TimestampAndNonce

# Get an instance of a logger
logger = logging.getLogger('LTI.lti_provider')


class LTIValidator(RequestValidator):
    """
    This validator implements the RequestValidator from the oauthlib.
    It implements only the methods required for a LTI request.
    """

    @property
    def enforce_ssl(self):
        """
        Returns false to not check for ssl.
        """
        logger.debug('called')
        return False

    @property
    def nonce_length(self):
        """
        Returns the min (5) and the max (50) length of a nonce.
        """
        return 5, 50

    @property
    def dummy_client(self):
        """
        Returns a dummy key used for false consumers.
        """
        logger.debug('called')
        return "dummy_client_key_123456"

    def get_client_secret(self, client_key, request):
        """
        Returns the secret of a consumer identified by its key.

        Keyword arguments:
            - client_key -- the key of the consumer
            - request -- calling request
        """
        logger.debug('called')
        try:
            c = Consumer.objects.get(key=client_key)
            return str(c.secret)
        except Consumer.DoesNotExist:
            return 'dummy_client_sec_123456'

    def validate_client_key(self, client_key, request):
        """
        Returns true if the given key exists.

        Keyword arguments:
            - client_key -- the key of the consumer
            - request -- calling request
        """
        logger.debug('called')
        try:
            n = Consumer.objects.filter(key=client_key).count()
            if n > 0:
                return True
            else:
                return False
        except Consumer.DoesNotExist:
            return False

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce,
                                     request, request_token=None,
                                     access_token=None):
        """
        Returns true if the given timestamp and nonce are valid for the
        consumer.

        Keyword arguments:
            - client_key -- the key of the consumer
            - timestamp -- the timestamp to validate
            - nonce -- the nonce to validate
            - request -- calling request
            - request_token -- unused for LTI
            - access_token -- unused for LTI
        """
        logger.debug('called')
        tn = TimestampAndNonce.objects.filter(
            consumer__key=client_key,
            timestamp=timestamp,
            nonce=nonce).count()
        if tn > 0:
            return False
        else:
            try:
                c = Consumer.objects.get(key=client_key)
            except Consumer.DoesNotExist:
                logger.debug('wrong consumer key')
                return False
            t = TimestampAndNonce(
                consumer=c,
                timestamp=timestamp,
                nonce=nonce)
            t.save()
            return True

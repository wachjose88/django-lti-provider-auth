
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
This module provides backends for the lti_provider.
"""

from hashlib import sha1

from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth.models import User

from lti_provider.utils import get_by_py_path
from lti_provider.validators import LTIValidator


class LTIAuthBackend(object):
    """
    This is a authentication backend for LTI.
    """

    def authenticate(self, request, tool_provider=None):
        """
        Authenticates a user via a LTI request from a consumer.

        Keyword arguments:
            - request -- the HttpRequest
            - tool_provider -- the LTI tool provider instance
        """
        if not tool_provider:
            return None

        validator = LTIValidator()
        ok = tool_provider.is_valid_request(validator)
        if not ok:
            raise PermissionDenied

        try:
            uid = tool_provider.launch_params['user_id']
        except KeyError:
            raise PermissionDenied
        try:
            email = tool_provider.launch_params[
                'lis_person_contact_email_primary']
        except KeyError:
            raise PermissionDenied
        try:
            given_name = tool_provider.launch_params['lis_person_name_given']
        except KeyError:
            given_name = 'LTI'
        try:
            family_name = tool_provider.launch_params['lis_person_name_family']
        except KeyError:
            family_name = 'LTI'

        username = email + '_' + sha1(uid.encode('utf-8')).hexdigest()
        username = username[:120]
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, password='LTI user')
            user.set_unusable_password()
            user.email = email
            user.first_name = given_name[:30]
            user.last_name = family_name[:30]
            user.save()
            try:
                hook = get_by_py_path(
                    settings.LTI_PROVIDER['HOOK_AFTER_USER_CREATION'])
                hook(user)
            except KeyError:
                pass

        if not user:
            raise PermissionDenied

        return user

    def get_user(self, user_id):
        """
        Returns a user object.

        Keyword arguments:
            - user_id -- the id of the user to return
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


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
This module provides the views of the lti_provider.
"""


import logging
from lti import ToolConfig
from lti.contrib.django import DjangoToolProvider
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from lti_provider.utils import reverse_from_settings

# Get an instance of a logger
logger = logging.getLogger('LTI.lti_provider')


@csrf_exempt
def tool_config(request):
    """
    This view returns a xml file with information about the LTI provider.

    Decorators:
        - csrf_exempt -- disable csrf protection

    Keyword arguments:
        - request -- calling HttpRequest
    """
    app_title = settings.LTI_PROVIDER['TITLE']
    app_description = settings.LTI_PROVIDER['DESCRIPTION']
    launch_url = request.build_absolute_uri(
        reverse('lti_provider.views.lti_launch'))

    lti_tool_config = ToolConfig(
        title=app_title,
        launch_url=launch_url,
        secure_launch_url=launch_url,
        description=app_description
    )

    return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')


@csrf_exempt
def lti_launch(request):
    """
    This is the entry point via LTI. It authenticates the user and redirects
    to the requested destination.

    Decorators:
        - csrf_exempt -- disable csrf protection

    Keyword arguments:
        - request -- calling HttpRequest
    """
    if request.user.is_authenticated():
        logout(request)

    try:
        tool_provider = DjangoToolProvider.from_django_request(request=request)
    except:
        return HttpResponseBadRequest('wrong config')

    user = authenticate(request=request, tool_provider=tool_provider)
    failed = settings.LTI_PROVIDER['FAILED_VIEW']
    if user is not None:
        if user.is_active:
            login(request, user)
            ps = settings.LTI_PROVIDER['PARAMETERS_TO_VIEW']
            for p in ps:
                ok = True
                ap = []
                for pn in p[0]:
                    gp = tool_provider.get_custom_param(pn)
                    ap.append(gp)
                    if not gp:
                        ok = False
                if ok:
                    try:
                        return HttpResponseRedirect(reverse(
                            p[1], args=ap))
                    except:
                        pass
            default = settings.LTI_PROVIDER['DEFAULT_VIEW']
            return HttpResponseRedirect(reverse_from_settings(default))
        else:
            return HttpResponseRedirect(reverse_from_settings(failed))
    else:
        return HttpResponseRedirect(reverse_from_settings(failed))

# Django LTI Provider with Authentication
This is a highly configurable LTI provider for Django projects with authentication. It is based on python3, python lti library and Django LTS. This library provides a Django app which implements a full LTI provider and could be used to let a user log in from another learning platform to your Django project. It handles the complete authentication of the user and after that it redirects to a view according to a configuration.

## Requirements
* python>=3.4
* Django>=1.11,<2.3
* lti>=0.9.2

## Install
To install the LTI provider for your Django project it is recommended to use pip:

```
pip3 install django-lti-provider-auth
```

Now add lti_provider to your INSTALLED_APPS in settings.py:

```
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ...
    'lti_provider.apps.LTIProviderConfig',
    ...
)
```

Add the authentication backend in settings.py:

```
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'lti_provider.backends.LTIAuthBackend',
]
```

Configure the LTI provider in settings.py:

```
LTI_PROVIDER = {
    'TITLE': 'name of your project',
    'DESCRIPTION': 'short description of your project',
    'DEFAULT_VIEW': ('example.views.index', (tuple of parameters or None)),
    'FAILED_VIEW': ('example.views.error', (tuple of parameters or None) ),
    'PARAMETERS_TO_VIEW': [
        (('example_parameter1', ), 'example.views.some_view'),
        (('example_parameter2', example_parameter3 ), 'example.views.some_other_view'),
        ...
    ],
    'HOOK_AFTER_USER_CREATION': 'example.utils.lti_after_user_creation'
}
```

The most important parts of the configuration are DEFAULT_VIEW, FAILED_VIEW and PARAMETERS_TO_VIEW because with them the redirection is configured.

* DEFAULT_VIEW: If no parameter is given by the LTI request this view is used as the goal of the redirection. It is a tuple where the first parameter is the name of the view and the second parameter is a tuple of parameters for the view or None.
* FAILED_VIEW: If something goes wrong this view is used. It is configured using the same format of a tuple as the DEFAULT_VIEW.
* PARAMETERS_TO_VIEW: It is possible to provide custom parameters through the LTI request. Depending on these parameters it is possible to redirect to a specific view. It should be a list of tuples. The first element of this tuple is a tuple of parameter names. The second element is the name of the view which is called if all of the listed parameter names are present in the LTI request. The values of the parameters are passed to the view while reversing it as keyword arguments using the name of the parameter as key.

The optional config entry HOOK_AFTER_USER_CREATION is the name of a function which takes a django user object as a parameter. This function is called after the creation of a new user.

The LTI provider requires the following parameters in the LTI request:

* lti_message_type: "basic-lti-launch-request"
* lti_version: 1
* resource_link_id: 1
* user_id: a unique user ID
* lis_person_name_given: first name of the user to login
* lis_person_name_family: last name of the user to login
* lis_person_contact_email_primary: email of the user to login, it is used as the username
* custom_<your custom parameter>: different parameters which should match with your configuration in PARAMETERS_TO_VIEW

Create the database entries:

```
python3 manage.py migrate
```

Finally add the URL configuration to your main urls.py:

```
urlpatterns = [
    ...
    url(r'^lti/', include('lti_provider.urls')),
    ...
]
```

## Usage
At first you have to create your LTI consumer at the admin site of your Django project. Here you have to specify an unique key and a secret token. Furthermore, each consumer has to be linked to a user account (e.g. the admin).

Now you can use your LTI provider at a consumer where you have to provide the following URL as a configuration: https:example.com/lti/config.xml

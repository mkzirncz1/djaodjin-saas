# Copyright (c) 2018, DjaoDjin inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Convenience module for access of saas application settings, which enforces
default settings when the main settings module does not contain
the appropriate settings.

The ``Organization`` broker manages the StripeConnect client account.

========================  ================= ===========
Name                      Default           Description
========================  ================= ===========
BROKER.GET_INSTANCE       basename(BASE_DIR)Slug for the ``Organization`` broker
                                            or callable that returns the
                                            ``Organization`` broker
                                            (useful for composition of Django
                                            apps).
BROKER.IS_INSTANCE_CALLABLE None            Function that will return `True`
                                            if the provider argument is the
                                            broker. If `None` we will compare
                                            provider with the instance returned
                                            by `BROKER.GET_INSTANCE`.
BYPASS_PERMISSION_CHECK    False            Skip all permission checks
BYPASS_PROCESSOR_AUTH      False            Do not check the auth token against
                                            the processor to set processor keys
                                            (useful to test StripeConnect).
EXTRA_MIXIN               object            Class to to inject into the parents
                                            of the Mixin hierarchy.
                                            (useful for composition of Django
                                            apps)
ORGANIZATION_MODEL        saas.Organization Replace the ``Organization`` model
                                            (useful for composition of Django
                                            apps)
PAGE_SIZE                 25                Maximum number of objects to return
                                            per API calls.
PROCESSOR                :doc:`Stripe backend<backends>`
PROCESSOR_ID             1                  pk of the processor ``Organization``
PROCESSOR_BACKEND_CALLABLE None             Optional function that returns
                                            the processor backend
                                            (useful for composition of Django
                                            apps).
PROVIDER_SITE_CALLABLE   None               Optional function that returns
                                            an object with a ``domain``
                                            field that is used to generate
                                            fully qualified URLs.
                                            (useful for composition of Django
                                            apps)
ROLE_RELATION            saas.Role          Replace the ``Role`` model
                                            (useful for composition of Django
                                            apps)
TERMS_OF_USE             'terms-of-use'     slug for the ``Agreement`` stating
                                            ther Terms of Use of the site.
========================  ================= ===========
"""
import os

from django.conf import settings

_SETTINGS = {
    'BYPASS_PERMISSION_CHECK': False,
    # Do not check the auth token against the processor to set processor keys.
    # (useful while testing).
    'BYPASS_PROCESSOR_AUTH': False,
    'DEFAULT_UNIT': 'usd',
    'EXPIRE_NOTICE_DAYS': [15],
    'EXTRA_MIXIN': object,
    'EXTRA_FIELD': None,
    'ORGANIZATION_MODEL': 'saas.Organization',
    'PAGE_SIZE': 25,
    'BROKER': {
        'GET_INSTANCE': os.path.basename(
            getattr(settings, 'BASE_DIR', "broker")),
        'IS_INSTANCE_CALLABLE': None,
        'BUILD_ABSOLUTE_URI_CALLABLE': None
    },
    'PROCESSOR': {
        'BACKEND': 'saas.backends.stripe_processor.StripeBackend',
        'CLIENT_ID': None,
        'FALLBACK': False,
        'INSTANCE_PK': 1,
        'MODE': 0,
        'PRIV_KEY': None,
        'PUB_KEY': None,
        'AUTHORIZE_CALLABLE': None,
        'REDIRECT_CALLABLE': None,
        'WEBHOOK_URL': 'stripe/postevent',
        'WEBHOOK_SECRET': None,
    },
    'PROCESSOR_BACKEND_CALLABLE': None,
    'ROLE_RELATION': 'saas.Role',
    'TERMS_OF_USE': 'terms-of-use',
    'PICTURE_STORAGE_CALLABLE': None,
}
_SETTINGS.update(getattr(settings, 'SAAS', {}))


ACCT_REGEX = r'[a-zA-Z0-9_\-\+\.]+'
MAYBE_EMAIL_REGEX = r'[a-zA-Z0-9_\-\+\.\@]+'
SELECTOR_RE = r'[a-zA-Z0-9_\-\:]+'
VERIFICATION_KEY_RE = r'[a-f0-9]{40}'
AUTH_USER_MODEL = getattr(
    settings, 'AUTH_USER_MODEL', 'django.contrib.auth.models.User')

BYPASS_PROCESSOR_AUTH = _SETTINGS.get('BYPASS_PROCESSOR_AUTH')
CREDIT_ON_CREATE = _SETTINGS.get('CREDIT_ON_CREATE')
EXPIRE_NOTICE_DAYS = _SETTINGS.get('EXPIRE_NOTICE_DAYS')
EXTRA_MIXIN = _SETTINGS.get('EXTRA_MIXIN')
ORGANIZATION_MODEL = _SETTINGS.get('ORGANIZATION_MODEL')
PAGE_SIZE = _SETTINGS.get('PAGE_SIZE')
PROCESSOR = _SETTINGS.get('PROCESSOR')
PROCESSOR_BACKEND_CALLABLE = _SETTINGS.get('PROCESSOR_BACKEND_CALLABLE')
PROCESSOR_FALLBACK = PROCESSOR.get('FALLBACK', [])
PROCESSOR_ID = PROCESSOR.get('INSTANCE_PK', 1)
PROCESSOR_HOOK_URL = PROCESSOR.get('WEBHOOK_URL', 'stripe/postevent')
PROCESSOR_HOOK_SECRET = PROCESSOR.get('WEBHOOK_SECRET')
BROKER_CALLABLE = _SETTINGS.get('BROKER').get('GET_INSTANCE', None)
IS_BROKER_CALLABLE = _SETTINGS.get('BROKER').get('IS_INSTANCE_CALLABLE', None)
BUILD_ABSOLUTE_URI_CALLABLE = _SETTINGS.get('BROKER').get(
    'BUILD_ABSOLUTE_URI_CALLABLE')
ROLE_RELATION = _SETTINGS.get('ROLE_RELATION')
TERMS_OF_USE = _SETTINGS.get('TERMS_OF_USE')
DEFAULT_UNIT = _SETTINGS.get('DEFAULT_UNIT')

# BE EXTRA CAREFUL! This variable is used to bypass PermissionDenied
# exceptions. It is solely intended as a debug flexibility nob.
BYPASS_PERMISSION_CHECK = _SETTINGS.get('BYPASS_PERMISSION_CHECK')

LOGIN_URL = getattr(settings, 'LOGIN_URL')
TIME_ZONE = getattr(settings, 'TIME_ZONE')
MANAGER = 'manager'
CONTRIBUTOR = 'contributor'

PICTURE_STORAGE_CALLABLE = _SETTINGS.get('PICTURE_STORAGE_CALLABLE')


def get_extra_field_class():
    extra_class = _SETTINGS.get('EXTRA_FIELD')
    if extra_class is None:
        from django.db.models import TextField
        extra_class = TextField
    elif isinstance(extra_class, str):
        from saas.compat import import_string
        extra_class = import_string(extra_class)
    return extra_class

# -*- coding: utf-8 -*-
from re import compile as regex

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


RE_CLASS = regex('').__class__


class SuperCacheMiddleware(MiddlewareMixin):

    """
    SuperCacheMiddleware provide fine tunning for Cache-Control
    HTTP header. By setting max age for urls you can control which
    pages/responses get cached in web browsers and frontend caching proxy.

    -----------
    Instalation
    -----------

    1. Put 'cas' in your INSTALLED_APPS
    INSTALLED_APPS = [
    ...
    'cas',
    ...
    ]

    2. Make sure this class is the FIRST in MIDDLEWARE_CLASSES
    in your settings.py
    MIDDLEWARE_CLASSES = [
    'cas.middleware.supercache.SuperCacheMiddleware',
    ...
    ]

    3. Set your prefered cache options in your settings.py

    ----------------
    Settings
    ----------------

    To set max age for, that will aggressivly cache views
          based on the following:
    - CACHE_DISABLED (bool) (default: False) switch caching off/on
    - CACHE_AJAX (bool) (default: False) enable ajax caching.
    - CACHE_AJAX_MAX_AGE (int) maximum caching time in seconds
    - CACHE_NORMAL_MAX_AGE (int) maximum caching time in seconds
    - CACHE_ULTRA_MAX_AGE (int) extended maximum caching time in seconds
    - CACHE_DISABLE_VARY (bool) (default: False) disable Vary header
          set it to True make cache more effecient
          WARNING: you need to configure CACHE_NEVER_REGEX
          for protected pages.
    - CACHE_AJAX_URL_REGEX (re.object) compiled regular expression for
          ajax requests.
    - CACHE_URL_REGEX (re.obj) compiled regular expression for noraml requests.
    - CACHE_ULTRA_REGEX (re.obj) compiled regular expression for
          extended cached.
    - CACHE_PRIVATE_REGEX (re.obj) compiled reqular expression for
         private cache.
    - CACHE_NEVER_REGEX (re.obj)(highest priority) compiled reqular
          expression for never cached requests for pages that need
          authentication/authorization.

    """

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        # get default settings
        self.cache_disabled = getattr(settings, 'CACHE_DISABLED', False)
        self.cache_ajax = getattr(settings, 'CACHE_AJAX',
                                  False)
        self.cache_ajax_max_age = getattr(settings, 'CACHE_AJAX_MAX_AGE',
                                          60 * 15)
        self.cache_normal_max_age = getattr(settings, 'CACHE_NORMAL_MAX_AGE',
                                            60 * 60 * 24)
        self.cache_ultra_max_age = getattr(settings, 'CACHE_ULTRA_MAX_AGE',
                                           60 * 60 * 24)
        self.cache_ajax_url_regex = getattr(settings, 'CACHE_AJAX_URL_REGEX',
                                            '')
        self.cache_url_regex = getattr(settings, 'CACHE_URL_REGEX',
                                       '')
        self.cache_ultra_url_regex = getattr(settings, 'CACHE_ULTRA_REGEX',
                                             '')
        self.cache_private_regex = getattr(settings, 'CACHE_PRIVATE_REGEX',
                                           '')
        self.cache_never_regex = getattr(settings, 'CACHE_NEVER_REGEX',
                                         '')
        self.cache_diable_vary = getattr(settings, 'CACHE_DISABLE_VARY',
                                         False)

    def process_response(self, request, response):
        if self.cache_disabled:
            return response

        if self.is_cachable(request):
            del response['Expires']
            ctype = 'public'
            if self.is_matched(self.cache_private_regex,
                               request.META['PATH_INFO']):
                ctype = 'private'
            if ctype == 'public' and self.cache_diable_vary:
                del response['Vary']
            response['Cache-Control'] = '%s, max-age=%d' % \
                (ctype, self.get_max_age(request))
        return response

    def is_cachable(self, request):
        if self.is_matched(self.cache_never_regex, request.META['PATH_INFO']):
            return False

        if request.is_ajax() and self.is_matched(
            self.cache_ajax_url_regex,
            request.META['PATH_INFO']) or \
                not request.is_ajax() and self.is_matched(
                    self.cache_ajax_url_regex,
                request.META['PATH_INFO']):
            return True

        return False

    def is_matched(self, val, path):
        if isinstance(val, RE_CLASS):
            return val.search(path) and True
        return False

    def get_max_age(self, request):

        if self.is_matched(self.cache_ultra_url_regex,
                           request.META['PATH_INFO']):
            return self.cache_ultra_max_age

        if request.is_ajax():
            return self.cache_ajax_max_age

        return self.cache_normal_max_age

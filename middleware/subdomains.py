# -*- coding: utf-8 -*-
from re import compile as regex

from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin


RE_CLASS = regex('').__class__


class SubdomainMiddleware(MiddlewareMixin):
    '''
    SubdomainMiddleware maps subdomains to apps
    For example an app named 'blog' which has url prefixed by 'blog'
    can be mapped to subdomain blog.example.com like:
    - Originally: https://www.example.com/blog/my-article
    - Becomes: https://blog.example.com/my-article
    or with i18n enabled as follows:
    - Originally: https://www.example.com/en/blog/my-article
    - Becomes: https://blog.example.com/en/my-article

    -----------
    Instalation
    -----------

    1. Put 'cas' in your INSTALLED_APPS
    INSTALLED_APPS = [
    ...
    'cas',
    ...
    ]

    2. Make sure this class is the last in MIDDLEWARE_CLASSES
    in your settings.py
    MIDDLEWARE_CLASSES = [
    ...
    'cas.middleware.subdomains.SubdomainMiddleware'
    ]

    3. Finally ajust the methods that generate urls in your app
    so that they don't contain app prefix, example of methods
    you want to change: get_absolute_url

    '''

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.lang_regex = getattr(settings, 'URL_LANG_REGEX', '')

    def process_request(self, request):
        try:
            resolve(request.path_info)
        except Resolver404:
            maps = getattr(settings, 'SUBDOMAINS_APPS_MAP', {})
            host = self.get_host(request)
            if host in maps:
                parts = self.get_path_parts(host. request.path_info)
                request.path_info = self.glue_path(parts)

    def get_host(request):
        return request.META['HTTP_HOST'].split(':')[0]

    def get_path_parts(self, app, path):
        parts = []
        lang_path = self.get_lang_path(path)
        parts.append(lang_path[0])
        parts.append(app)
        parts.append(lang_path[1])
        return parts

    def is_i18n(self):
        if getattr(settings, 'USE_I18N', False):
            return True
        return False

    def get_lang_path(self, path):
        if not self.is_i18n() or \
           not isinstance(self.lang_regex, RE_CLASS):
            return ['', path]
        lang = self.lang_regex.search(path)
        lang = lang.strip('/')
        return [lang, path.strip('/').replace('//',  '/')]

    def glue_path(self, *parts):
        url = '/'
        for u in parts:
            u = u.strip('/')
            if u:
                url += u + '/'
        if not getattr(settings, 'APPEND_SLASH', True):
            return url.rstrip('/')
        return url

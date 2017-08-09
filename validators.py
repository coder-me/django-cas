# -*- coding: utf-8 -*-
from re import compile as regex

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def zeroslash_slug(value):
    '''
    validate if a value is a valid slug with no slashes
    valid slugs those don't contain any of the following chars:
    ! @ ~ # \ > < : ; [ ] { } % & * ( ) $ / \s ?
    '''
    re = r'^[^!@~#\\\\><:;\[\]\{\}%&\*\(\)\$/\s\?]+$'
    RegexValidator(re, r'Invalid Slug Value').__call__(value)


def oneslash_slug(value):
    '''
    validate if a value is a valid slug
    valid slugs those don't contain any of the following chars:
    ! @ ~ # \ > < : ; [ ] { } % & * ( ) $ \s ?
    and they are in the form of two slugs seprated by
    one slash
    '''
    re = r'^[^!@~#\\\\><:;\[\]\{\}%&\*\(\)\$/\s\?]+$'
    RegexValidator(
        re,
        r'Invalid Slug Value, value should contain one slash').__call__(value)


def valid_regex(value):
    """
    Validate if a value is a valid regular expression
    """
    try:
        regex(value)
    except:
        raise ValidationError('Invalid regex')

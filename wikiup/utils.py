#!/usr/bin/env python3.6
# vim: set fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4 smarttab autoindent:
# -*- coding: utf-8 -*-


"""wikiup.utils"""

import os
import getpass
from bs4.dammit import EntitySubstitution


def require_password(password: str=None):
    if not password:
        return_ = getpass.getpass()
    else:
        return_ = password
    return str(return_)


def get_option(opt: str, args: dict) -> str:
    opt_env = 'WIKIUP_{}'.format(opt.upper())
    if opt_env in os.environ.keys():
        return os.environ[opt_env]
    else:
        return args['--{}'.format(opt)]


def compose_url(wid):
    protocol = 'https'
    target_host = 'wiki.signetaccel.com'
    target_path = '/rest/api/content'

    url = f'{protocol}://{target_host}{target_path}/{wid}'

    return url


def non_newlines(tag):
    return str(tag) != '\n'


def custom_formatter(string):
    """add &quot; and &apos; to entity substitution"""
    # return EntitySubstitution.substitute_html(string).replace('"', '&quot;').replace("'", '&apos;')
    return EntitySubstitution.substitute_html(string).replace('"', '&quot;')

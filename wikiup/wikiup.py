#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""wikiup

Usage:
    wikiup update (-m <file> | --markdown <file>) (-w <wid> | --wiki-id <wid>) [-s <space> | --space <space>]
                [-u <username> | --username <username>] [-p <password> | --password <password>]
                [-t | --trim-h1]

    wikiup export (-w <wid> | --wiki-id <wid>) (-o <outfile> | --outfile=<outfile>)

    wikiup -h | --help
    wikiup --version

Options:
    -m <file> --markdown=<file>          Input markdown file
    -w <wid> --wiki-id=<wid>             Destination wiki page ID
    -s <space> --space=<space>           Destination wiki page space (eg. "SYS" for "System Administration")
    -u <username> --username=<username>  Username [default: jdoe]
    -p <password> --password=<password>  Password [default: nopassword]
    -t --trim-h1                         Trim the first level 1 header (useful if used as title in document content) [default: False]
    -o <outfile> --outfile=<outfile>     File to export data to

    -h --help                            Show this screen
    --version                            Show version

Any long-form option (id, file, profile, etc.) may also be specified as an environment variable of the form WIKIUP_$VAR
where $VAR is the option in upper case.  Specifying an environment variable takes precedence of the CLI option.

"space", "username", and "password" are required parameters even though the usage states optional.  This is to allow
them to be specified as environment variables.

"""

# from __future__ import unicode_literals, print_function

import os
# import json
from requests import get, put
import re
from docopt import docopt
from paka import cmark
from bs4 import BeautifulSoup, element
from copy import deepcopy
import difflib

__author__ = 'Jesse Butcher'
__email__ = 'jbutcher@signetaccel.com'
__version__ = '0.1.0'


def compose_url(wid):
    protocol = 'https'
    target_host = 'wiki.signetaccel.com'
    target_path = '/rest/api/content'

    url = f'{protocol}://{target_host}{target_path}/{wid}'

    return url


def get_option(opt: str, args: dict) -> str:
    opt_env = 'WIKIUP_{}'.format(opt.upper())
    if opt_env in os.environ.keys():
        return os.environ[opt_env]
    else:
        return args['--{}'.format(opt)]


def get_latest(url, auth, parameters):
    response = get(url, auth=auth, params=parameters)
    if response.status_code == 200:
        if response.headers['Content-Type'] == 'application/json':
            # print(json.dumps(response.json(), indent=4))
            pass

    return response.json()


def compose_data(obj, data_in=""):

    if data_in != obj['body']['storage']['value']:
        a = data_in.splitlines()
        b = obj['body']['storage']['value'].splitlines()
        diff = difflib.unified_diff(a, b, 'Scraped from Wiki', 'Parsed Markdown', lineterm="")
        print('\n'.join(list(diff)))
        print('\nConfirm change')
        input("Press Enter to continue...")

        changed = True
        data_out = {
            "id": obj['id'],
            "type": obj['type'],
            "title": obj['title'],
            "space": {
                "key": obj['space']['key']
            },
            "body": {
                "storage": {
                    "value": data_in,
                    "representation": "storage"
                }
            },
            "version": {
                "number": obj['version']['number'] + 1
            }
        }
    else:
        changed = False
        data_out = ""
        print('WARN :: No change in data')

    return changed, data_out


def put_(url, auth, data):
    response = put(url, auth=auth, json=data)

    return response.status_code


def parse_md(file_in):
    with open(file_in, 'r') as f:
        read_md = f.read()
    md = cmark.to_html(read_md, safe=True)
    # md = '<p>Test</p>'

    soup = BeautifulSoup(md, 'html.parser')

    # Remove Marxico line
    marxico = soup.find_all('p', string=re.compile('@\(Marxico\).*'))
    if marxico:
        marxico[0].decompose()

    # Remove [TOC] line
    toc = soup.find_all('p', string=re.compile('.*\[TOC\].*'))
    if toc:
        toc[0].decompose()

    # Remove <h1> line
    h1_list = soup.find_all('h1')
    if len(h1_list) > 1:
        print('More than one <h1> found.  I don\'t know what to do')
        exit(1)
    elif len(h1_list) == 1:
        soup.h1.decompose()

    # If first element is <hr>, remove it
    soup_string = str(soup).lstrip().rstrip()
    soup2 = BeautifulSoup(soup_string, 'html.parser')
    first_hr = soup2.find_all('hr', limit=1)[0]
    if soup2.contents[0] == first_hr:
        first_hr.decompose()

    for code_block in soup2.find_all('pre'):
        new = soup.new_tag('ac:structured-macro')
        new.attrs['ac:name'] = 'code'
        new_p1 = soup.new_tag('ac:parameter')
        new_p1.attrs['ac:name'] = 'theme'
        new_p1.string = 'Midnight'
        new_p2 = soup.new_tag('ac:parameter')
        new_p2.attrs['ac:name'] = 'language'
        new_p2.string = code_block.code.attrs['class'][0].split('-')[1]
        new_body = soup.new_tag('ac:plain-text-body')

        new_body.string = element.CData(code_block.code.string)

        new.append(new_p1)
        new.append(new_p2)
        new.append(new_body)

        code_block.replace_with(new)

    # Clean up
    from bs4.dammit import EntitySubstitution

    def custom_formatter(string):
        """add &quot; and &apos; to entity substitution"""
        # return EntitySubstitution.substitute_html(string).replace('"', '&quot;').replace("'", '&apos;')
        return EntitySubstitution.substitute_html(string).replace('"', '&quot;')

    soup2_string = soup2.encode(formatter=custom_formatter).lstrip().rstrip()

    reg = re.compile(r'REDACT(<|&lt;)-{2,}.+-{2,}(>|&gt;)', re.MULTILINE)
    soup2_string = re.sub(reg, '[--REDACTED--]', soup2_string.decode(encoding='utf-8'))

    return soup2_string


def main():
    """Main entry point for the wikiup CLI.
    """
    args = docopt(__doc__, version=__version__)
    # args_pp = json.dumps(args, indent=4)
    # print(f'args: {args_pp}')

    if args['update']:
        file_in = get_option('markdown', args)
        auth = (get_option('username', args), get_option('password', args))
        url = compose_url(wid=get_option('wiki-id', args))
        # print(f'file_in: {file_in}\nauth: {auth}\nurl: {url}\n')
        space = get_option('space', args)
        parameters = {
            'type': 'page',
            'spaceKey': space,
            'expand': 'body.storage,version,space'
        }

        latest = get_latest(url, auth, parameters)

        md = parse_md(file_in)
        data_changed, data = compose_data(latest, md)
        if data_changed:
            data_terse = deepcopy(data)
            data_terse['body']['storage']['value'] = '...'
            print(f'Putting: {data_terse}')

            sc = put_(url, auth, data)
            print(f'Status Code: {sc}')
    elif args['export']:
        # TODO
        raise NotImplementedError

if __name__ == '__main__':
    main()

# vim:fileencoding=utf-8

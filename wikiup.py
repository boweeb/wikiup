#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""wikiup

Usage:
  wikiup update

  wikiup -h | --help
  wikiup --version

Any long-form option (id, file, profile, etc.) may also be specified as an environment variable of the form QUERV_$VAR
where $VAR is the option in upper case.  Specifying an environment variable takes precedence of the CLI option.

"""

# from __future__ import unicode_literals, print_function

# import os
# import json
from requests import get, put
import re
from docopt import docopt
from paka import cmark
from bs4 import BeautifulSoup, element
from copy import deepcopy
import difflib

__author__ = 'Jesse Butcher'
__email__ = 'boweeb@gmail.com'
__version__ = '0.1.0'


# 3407907 -- Test
# 2728955 -- Dog Tag
# 2725585 -- Ansible

PID = 3407907
USER_ = ''
PASS_ = ''

FILE_IN = '/Users/jbutcher/Documents/Notes/hq-ca0.md'

PROTOCOL = 'https'
TARGET_HOST = 'wiki.signetaccel.com'
TARGET_PATH = '/rest/api/content'

PARAMETERS_ = {
    'type': 'page',
    'spaceKey': 'SYS',
    'expand': 'body.storage,version,space'
}


URL = f'{PROTOCOL}://{TARGET_HOST}{TARGET_PATH}/{PID}'


def get_latest():
    response = get(URL, auth=(USER_, PASS_), params=PARAMETERS_)
    # response = get(URL, auth=(USER_, PASS_))
    if response.status_code == 200:
        if response.headers['Content-Type'] == 'application/json':
            # print(json.dumps(response.json(), indent=4))
            pass

    return response.json()


def compose_data(obj, data_in=""):

    if data_in != obj['body']['storage']['value']:
        a = data_in.splitlines()
        b = obj['body']['storage']['value'].splitlines()
        diff = difflib.unified_diff(a, b, 'Parsed Markdown', 'Scraped from Wiki', lineterm="")
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


def put_(data):
    response = put(URL, auth=(USER_, PASS_), json=data, )

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

    # for string in soup.strings:
    #     string.replace_with(string.replace('"', '&quot;'))

    # soup2_string = str(soup2).lstrip().rstrip()
    soup2_string = soup2.encode(formatter=custom_formatter).lstrip().rstrip()

    # print(soup2_string)
    # exit()
    return soup2_string.decode(encoding='utf-8')


def main():
    """Main entry point for the wikiup CLI.
    """
    args = docopt(__doc__, version=__version__)
    # args_pp = json.dumps(args, indent=4)
    # print(f'args: {args_pp}')

    if args.update:
        latest = get_latest()

        md = parse_md(FILE_IN)
        data_changed, data = compose_data(latest, md)
        if data_changed:
            data_terse = deepcopy(data)
            data_terse['body']['storage']['value'] = '...'
            print(f'Putting: {data_terse}')

            sc = put_(data)
            print(f'Status Code: {sc}')


if __name__ == '__main__':
    main()

# vim:fileencoding=utf-8

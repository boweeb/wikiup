#!/usr/bin/env python3.6
# vim: set fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4 smarttab autoindent:
# -*- coding: utf-8 -*-


"""wikiup.document"""


import re
from pathlib import Path

from bs4 import BeautifulSoup, element
from paka import cmark

from .config import GlobalConfig
from .utils import non_newlines, custom_formatter


C = GlobalConfig()


class MarkdownDocument(object):
    def __init__(self, manifest):
        self.manifest = manifest

        self.content = None

        self._parse()
        self._soup = BeautifulSoup(self.content, 'html.parser')
        self._transform()

        self.input_md_filename = Path(self.manifest['file_in']).name

    def __str__(self):
        return self.input_md_filename

    def __bytes__(self):
        return self.input_md_filename

    def __repr__(self):
        file_in = self.manifest['file_in']
        return f'<MarkdownDocument: path="{file_in}">'

    def _parse(self):
        with open(self.manifest['file_in'], 'r') as f:
            file = f.read()

        self.content = cmark.to_html(file, safe=True)

    def _strip_marxico(self):
        # Remove Marxico line
        marxico = self._soup.find_all('p', string=re.compile(r'@\(Marxico\).*'))
        if marxico:
            marxico[0].decompose()

        # Remove [TOC] line
        toc = self._soup.find_all('p', string=re.compile(r'.*\[TOC\].*'))
        if toc:
            toc[0].decompose()

        # Remove <h1> line
        h1_list = self._soup.find_all('h1')
        if len(h1_list) > 1:
            print('More than one <h1> found.  I don\'t know what to do')
            exit(1)
        elif len(h1_list) == 1:
            self._soup.h1.decompose()

        # If first non-newline tag is <hr/>, remove it
        first_non_newline = self._soup.find_all(non_newlines)[0]
        if str(first_non_newline) == '<hr/>':
            first_non_newline.decompose()

    def _convert_codeblocks(self):
        for code_block in self._soup.find_all('pre'):
            new_cb_tag = self._soup.new_tag('ac:structured-macro')
            new_cb_tag.attrs['ac:name'] = 'code'
            cb_theme = self._soup.new_tag('ac:parameter')
            cb_theme.attrs['ac:name'] = 'theme'
            # TODO: make theme configurable
            cb_theme.string = C.theme
            cb_language = self._soup.new_tag('ac:parameter')
            cb_language.attrs['ac:name'] = 'language'
            cb_language.string = code_block.code.attrs['class'][0].split('-')[1]
            cb_content = self._soup.new_tag('ac:plain-text-body')

            cb_content.string = element.CData(code_block.code.string)

            new_cb_tag.append(cb_theme)
            new_cb_tag.append(cb_language)
            new_cb_tag.append(cb_content)

            code_block.replace_with(new_cb_tag)

    def _clean(self):
        # Export string for regex to operate on
        # custom_formatter: Always replace " (double-quote) with "&quot;"
        soup_string = self._soup.encode(formatter=custom_formatter).lstrip().rstrip()

        # Replace redaction tagged text with redaction text
        soup_string = re.sub(C.redact_re,
                             C.redaction_replacement_text,
                             soup_string.decode(encoding='utf-8'))

        return soup_string

    def _transform(self):

        # These mutate self.soup
        if C.strip_marxico:
            self._strip_marxico()
        if C.convert_codeblocks:
            self._convert_codeblocks()

        self.content = self._clean()

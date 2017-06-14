#!/usr/bin/env python3.6
# vim: set fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4 smarttab autoindent:
# -*- coding: utf-8 -*-


"""wikiup.broker"""


import difflib


class Broker(object):
    def __init__(self, markdown_document, wiki_page):
        self.md = markdown_document
        self.page = wiki_page
        self.dirty = self._diff()

    def _diff(self):
        if self.md.content != self.page.content:
            dirty = True
        else:
            dirty = False
            print('INFO :: No change in data')

        return dirty

    def upload(self):
        self.page.put(self.md.content)
        self.page.get()
        self.dirty = self._diff()

    def prompt_continue(self):
        a = self.page.content.splitlines()
        b = self.md.content.splitlines()
        diff = difflib.unified_diff(a, b, 'Scraped from Wiki', 'Parsed Markdown', lineterm="")
        print('\n'.join(list(diff)))
        print('\nConfirm change')
        input("Press Enter to continue...")

#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4 smarttab autoindent:
# -*- coding: utf8 -*-


"""wikiup.config:  This tool pulls in config options and creates globals."""


import os
import re
import configparser
from xdg import BaseDirectory
# from nohands.options import CLIOptions as O


def dir_check(directory):
    """ Check if directory exists, if not then create it. """
    # print("Checking if \"{}\" exists... ".format(directory), end='')
    try:
        os.makedirs(directory)
        print("Directory did not exist. Created \"{}\"".format(directory))
    except OSError:
        if not os.path.isdir(directory):
            raise


class GlobalConfig:
    """Global Config"""

    def __init__(self):
        """ Constructor """

        self.project_name = 'wikiup'

        xdg_config_home = os.path.abspath(BaseDirectory.xdg_config_home)
        xdg_data_home = os.path.abspath(BaseDirectory.xdg_data_home)
        self.config_home = os.path.join(xdg_config_home, self.project_name)
        self.data_home = os.path.join(xdg_data_home, self.project_name)
        dir_check(self.config_home)
        dir_check(self.data_home)

        self.config_file = os.path.join(self.config_home, "config.ini")

        self.config = configparser.ConfigParser()
        # And if config.ini doesn't exist, init a blank one.
        if not os.path.exists(self.config_file):
            print("Config file missing. Initializing new, blank one.")
            with open(self.config_file, "w") as fp:
                fp.write("[Settings]\n" +
                         "strip_marxico = False\n" +
                         "convert_codeblocks = True\n" +
                         "redaction_replacement_text = \"[--REDACTED--]\"\n" +
                         "\n" +
                         "[CodeBlocks]\n" +
                         "theme = Midnight\n" +
                         "\n" +
                         "[Bookmarks]\n" +
                         "theme = Midnight\n" +
                         "\n"
                         )

        self.config.read(self.config_file)

        # --------------------------------------------------------------------
        # CONFIG FILE:

        # [Settings]
        sec = 'Settings'
        self.strip_marxico = self.config.getboolean(sec, 'strip_marxico')
        self.convert_codeblocks = self.config.getboolean(sec, 'convert_codeblocks')
        self.redaction_replacement_text = self.config.get(sec, 'redaction_replacement_text')

        # [CodeBlocks]
        sec = 'CodeBlocks'
        self.theme = self.config.get(sec, 'theme')

        # --------------------------------------------------------------------
        # CONSTANTS:

        # self.x = 'y'

        # --------------------------------------------------------------------
        # REGEX:

        # ASCII printable characters
        ascii_chars = ''.join(map(chr, range(32, 127)))
        self.ascii_char_re = re.compile('[{}]'.format(re.escape(ascii_chars)))

        # Match a "redact" tag
        self.redact_re = re.compile(r'REDACT(<|&lt;)-{2,}.+-{2,}(>|&gt;)', re.MULTILINE)

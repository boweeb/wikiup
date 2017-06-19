#!/usr/bin/env python3.6
# vim: set fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4 smarttab autoindent:
# -*- coding: utf-8 -*-


"""wikiup

Sync up a local markdown file to a Confluence wiki page

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
    -u <username> --username=<username>  Username (will default to shell's $USER)
    -p <password> --password=<password>  Password (if not provided will prompt for input)
    -t --trim-h1                         Trim the first level 1 header (useful if used as title in document content)
                                         [default: False]
    -o <outfile> --outfile=<outfile>     File to export data to

    -h --help                            Show this screen
    --version                            Show version

Notes:
    Any long-form option (id, file, profile, etc.) may also be specified as an environment variable of the form
    WIKIUP_$VAR where $VAR is the option in upper case.  Specifying an environment variable takes precedence of the CLI
    option.

    "space", "username", and "password" are required parameters even though the usage states optional.  This is to allow
    them to be specified as environment variables.

Examples:
    The following are equivalent:

    # wikiup update -m "~/Documents/foobar.md" -w 123456789 -s FOO -u johnsmith -p "bAdp@ssw0rD"

    and

    # WIKIUP_USERNAME=johnsmith
    # WIKIUP_PASSWORD="bAdp@ssw0rD"
    # wikiup update -m "~/Documents/foobar.md" -w 123456789 -s FOO

"""


from docopt import docopt

# from .config import GlobalConfig
from .document import MarkdownDocument
from .page import WikiPage
from .broker import Broker
from .utils import get_option, compose_url, require_password, get_shell_username


__author__ = """Jesse Butcher"""
__email__ = 'jbutcher@signetaccel.com'
__version__ = '0.2.3'


# C = GlobalConfig()


def main():
    """Main entry point for the wikiup CLI.
    """
    args = docopt(__doc__, version=__version__)
    # args_pp = json.dumps(args, indent=4)
    # print(f'args: {args_pp}')

    if args['update']:
        username = get_shell_username(get_option('username', args))
        password = require_password(get_option('password', args))

        manifest = {
            'markdown': {
                'file_in': get_option('markdown', args),
            },
            'page': {
                'auth': (username, password),
                'url': compose_url(wid=get_option('wiki-id', args)),
                'slug': get_option('wiki-id', args),
                'parameters': {
                    'type': 'page',
                    'spaceKey': get_option('space', args),
                    'expand': 'body.storage,version,space'
                }
            }
        }

        md = MarkdownDocument(manifest['markdown'])
        page = WikiPage(manifest['page'])
        broker = Broker(md, page)

        if broker.dirty:
            broker.prompt_continue()
            broker.upload()

    elif args['export']:
        # TODO
        raise NotImplementedError

if __name__ == '__main__':
    main()

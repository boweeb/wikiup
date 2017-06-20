======
wikiup
======

Sync up a local markdown file to a Confluence wiki page

`wikiup` uses CommonMark as it's markdown processor so the most canonical references should specifically mention
"commonmark".

* CommonMark website_

  - http://spec.commonmark.org -- The CommonMark specification.
  - http://code.commonmark.org -- Reference implementation and validation test suite on GitHub.
  - http://talk.commonmark.org -- Public discussion area and mailing list.
  - http://commonmark.org/help -- Quick reference card and interactive tutorial for learning Markdown.
  - http://try.commonmark.org -- Live testing tool powered by the reference implementation.

* Free software: ISC license
* Documentation: https://git0.signetaccel.net/admintools/wikiup/wikis/home.


Features
--------

* TODO


Requirements
------------

* Python >= 3.6
* libffi
  - EL: `libffi-devel`
  - Debian: `libffi-dev`


TODO
----

* [*Feature*] Option to include table of contents macro at top of page.
* [*Feature*] Implement a bookmark system to easily reference pairs of markdown files and destination wiki pages.
* [*Core*] Replace `print` statements with proper implementation of `logging` module
* [*Core*] Handle errors from markdown processor
* [*Feature*] Offer choice to save `md.contents` and `page.contents` to files for offline `diff` comparison.
* [*Core*] Allow an optional git-based workflow for storing markdown files

  - wiki pages get updated after a post-commit trigger
  - wiki pages should have head note to the effect of, "This page is wikiup controlled. Only makes edits from repo!"
  - `wikiup` becomes a backend tool and the UX changes to `git commit`.

* [*Core*] Make the "continue if you approve diff" prompt more flexible, accepting more/different actions
* [*Feature*] Add auto-accept flag and standardize a "silent"/"unattended" mode


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _website: http://commonmark.org
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

#!/usr/bin/env python3.6
# vim: set fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4 smarttab autoindent:
# -*- coding: utf-8 -*-


"""wikiup.page"""


from requests import get as r_get, put as r_put


class WikiPage(object):
    def __init__(self, manifest):
        self.manifest = manifest

        self.data = None
        self.get_result_code = None
        self.put_result_code = None

        self.get()
        self.content = self.data['body']['storage']['value']

    def __str__(self):
        slug = self.manifest['slug']
        space = self.manifest['parameters']['spaceKey']
        return f'{space}:{slug}'

    def __bytes__(self):
        slug = self.manifest['slug']
        space = self.manifest['parameters']['spaceKey']
        return f'{space}:{slug}'

    def __repr__(self):
        url = self.manifest['url']
        return f'<WikiPage: url="{url}">'

    def get(self):
        response = r_get(
            url=self.manifest['url'],
            auth=self.manifest['auth'],
            params=self.manifest['parameters'])
        if response.status_code == 200:
            if response.headers['Content-Type'] == 'application/json':
                # print(json.dumps(response.json(), indent=4))
                pass

        self.data = response.json()
        self.get_result_code = response.status_code

        print(f'INFO :: GET Result Code = {self.get_result_code}')

    def put(self, new_content):
        datagram = self._compose_datagram(
            obj=self.data,
            new_content=new_content
        )
        response = r_put(
            url=self.manifest['url'],
            auth=self.manifest['auth'],
            json=datagram
        )

        self.put_result_code = response.status_code

        print(f'INFO :: PUT Result Code = {response.status_code}')

    @staticmethod
    def _compose_datagram(obj, new_content):
        datagram = {
            "id": obj['id'],
            "type": obj['type'],
            "title": obj['title'],
            "space": {
                "key": obj['space']['key']
            },
            "body": {
                "storage": {
                    "value": new_content,
                    "representation": "storage"
                }
            },
            "version": {
                "number": obj['version']['number'] + 1
            }
        }

        return datagram

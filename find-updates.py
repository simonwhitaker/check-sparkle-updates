#!/usr/bin/env python3

from typing import Any, Dict, List;

import os
import plistlib

class App(object):
    def __init__(self, path):
        self._path = path
        self._info = None

    def __str__(self):
        return self.path

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return os.path.basename(self.path).split('.app')[0]

    @property
    def info(self) -> Dict[str, Any]:
        if self._info is None:
            info_plist = os.path.join(self.path, 'Contents', 'Info.plist')
            with open(info_plist, 'rb') as f:
                self._info = plistlib.load(f)
        return self._info

    @property
    def sparkle_feed_url(self) -> str:
        try:
            url = self.info['SUFeedURL'].strip()
            if len(url) == 0:
                raise App.NoSparkleFeedURLException
            return url
        except KeyError:
            raise App.NoSparkleFeedURLException

    @property
    def version(self) -> str:
        return self.info['CFBundleShortVersionString']

    class NoSparkleFeedURLException(Exception):
        pass

def find_apps(dirs: List[str]) -> List[App]:
    for dir in dirs:
        for f in os.listdir(dir):
            if f.endswith('.app'):
                yield App(os.path.join(dir, f))

if __name__ == "__main__":
    for app in find_apps(['/Applications', os.path.expanduser('~/Applications')]):
        try:
            print("{0} ({1}): {2}".format(app.name, app.version, app.sparkle_feed_url))
        except:
            # print("{0} doesn't use Sparkle".format(app.name()))
            pass

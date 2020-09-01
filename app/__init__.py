import os
import plistlib

from typing import Any, Dict

from sparkle import SparkleFeed


class App(object):
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(self.path).split('.app')[0]
        self._info = None

    def __str__(self):
        return self.path

    def info(self) -> Dict[str, Any]:
        if self._info is None:
            info_plist = os.path.join(self.path, 'Contents', 'Info.plist')
            with open(info_plist, 'rb') as f:
                self._info = plistlib.load(f)
        return self._info

    def sparkle_feed(self) -> SparkleFeed:
        try:
            url = self.info()['SUFeedURL'].strip()
            if len(url) > 0:
                return SparkleFeed(url)
        except KeyError:
            pass
        raise NoSparkleFeedURLException

    def version(self) -> str:
        return self.info()['CFBundleVersion']


class NoSparkleFeedURLException(Exception):
    pass

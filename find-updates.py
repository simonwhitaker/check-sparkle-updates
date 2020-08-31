#!/usr/bin/env python3

import os
import plistlib

from operator import attrgetter
from typing import Any, Dict, List;

from app import App, NoSparkleFeedURLException

def find_apps(dirs: List[str]) -> List[App]:
    for dir in dirs:
        for f in os.listdir(dir):
            if f.endswith('.app'):
                yield App(os.path.join(dir, f))

if __name__ == "__main__":
    apps = find_apps([
        '/Applications',
        os.path.expanduser('~/Applications'),
    ])
    for app in apps:
        if app.name == 'VLC':
            # The VLC sparkle URL is timing out at the moment (2020-08-30),
            # let's ignore it.
            # TODO: add timeout support when fetching RSS feeds
            continue
        try:
            if app.version == app.sparkle_feed.latest_version:
                print("{0} is up to date".format(app.name))
            else:
                print("{0}: {1} -> {2}".format(
                    app.name,
                    app.version,
                    app.sparkle_feed.latest_version
                ))
        except NoSparkleFeedURLException:
            # The app doesn't use Sparkle for updates. Ignore it.
            pass
        except Exception as e:
            print("{0}: Unexpected error: {1}".format(app.name, e))

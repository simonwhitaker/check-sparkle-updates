#!/usr/bin/env python3

import os
import plistlib

from operator import attrgetter
from traceback import print_tb
from typing import List

from app import App, NoSparkleFeedURLException
from termcolor import cprint


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
            local_version = app.version()
            sparkle_version = app.sparkle_feed().latest_version()
            if sparkle_version > local_version:
                cprint("{0}: {1} -> {2}".format(
                    app.name,
                    local_version,
                    sparkle_version
                ), attrs=['bold'])
            elif sparkle_version < local_version:
                cprint("Hmm... you have version {1} of {0}, but sparkle only has {2}".format(
                    app.name, local_version, sparkle_version), 'yellow')
            else:
                cprint(
                    "{0} is up to date (you have {1}, sparkle has {2})".format(
                        app.name,
                        local_version,
                        sparkle_version),
                    attrs=['dark'])
        except NoSparkleFeedURLException:
            # The app doesn't use Sparkle for updates. Ignore it.
            pass
        except Exception as e:
            print("{0}: Unexpected error: {1}".format(app.name, e))
            print_tb(e.__traceback__)

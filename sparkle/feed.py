import feedparser

from operator import attrgetter
from typing import List

from sparkle.version import SparkleVersion

class SparkleEntry(object):
    def __init__(self, entry):
        self.entry = entry
        sparkle_links = [l for l in entry.links if 'sparkle:version' in l]
        # We might have multiple sparkle links here, e.g. if the app supports
        # delta updates (see e.g. https://coderunnerapp.com/appcast.xml), but
        # they should all have the same sparkle:version, so just use the first.
        self.version = SparkleVersion(sparkle_links[0]['sparkle:version'])

class SparkleFeed(object):
    def __init__(self, url: str):
        self._url = url
        self._payload = None
        self._entries = []

    def payload(self) -> feedparser.FeedParserDict:
        if self._payload is None:
            self._payload = feedparser.parse(self._url)
        return self._payload

    def entries(self) -> List[SparkleEntry]:
        return [SparkleEntry(e) for e in self.payload().entries if any(
            ['sparkle:version' in link for link in e.links]
        )]

    def latest_version(self) -> str:
        sorted_entries = sorted(
            self.entries(),
            key=attrgetter('version'),
            reverse=True
        )
        if len(sorted_entries) == 0:
            return '0'
        return sorted_entries[0].version.version_string

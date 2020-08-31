import feedparser

class SparkleFeed(object):
    def __init__(self, url: str):
        self._url = url
        self._payload = None

    @property
    def payload(self) -> feedparser.FeedParserDict:
        if self._payload is None:
            self._payload = feedparser.parse(self._url)
        return self._payload

    @property
    def latest_version(self) -> str:
        entries = self.payload.entries
        # TODO: sort by version string. Apps can provide their own version
        # comparator function, but the default logic used by Sparkle is here:
        # https://github.com/sparkle-project/Sparkle/blob/master/Sparkle/SUStandardVersionComparator.m
        return entries[0].links[0]['sparkle:version']

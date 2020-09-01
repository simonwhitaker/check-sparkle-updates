import re

from functools import total_ordering
from typing import List;

@total_ordering
class SparkleVersion(object):
    def __init__(self, version: str):
        self.version_string = version

    def version_parts(self) -> List[str]:
        # Ignore hyphens and anything after them
        v = self.version_string.split('-')[0]
        return re.split(r'\W', v)

    def __eq__(self, other):
        return self.version_parts() == other.version_parts()

    def __lt__(self, other):
        self_parts = self.version_parts()
        other_parts = other.version_parts()

        # Compare the two versions up to and including the final index of the
        # shorter set of parts.
        for (a, b) in zip(self_parts, other_parts):
            if a == b:
                continue
            if a.isdigit() and b.isdigit():
                return int(a) < int(b)
            # Next two checks: Sparkle treats numbers as greater than strings
            elif a.isdigit() and not b.isdigit():
                return False
            elif b.isdigit() and not a.isdigit():
                return True
            else:
                return a < b

        # If we got this far either the versions are identical, or one has more
        # parts than the other. If other has more parts than self, then we'll
        # treat it as a higher version (e.g. 1.1 vs 1.1.1)
        return len(self_parts) < len(other_parts)

from collections import namedtuple

__version__ = "1.1.1a"

VersionInfo = namedtuple("VersionInfo", "major minor macro release")

version_info = VersionInfo(1, 1, 1, "alpha")

from dataclasses import dataclass

__version__ = "1.1.1a6"


@dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


version_info = VersionInfo(1, 1, 1, "alpha", 6)

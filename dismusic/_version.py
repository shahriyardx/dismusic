from dataclasses import dataclass

__version__ = "1.2.1"


@dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


version_info = VersionInfo(1, 2, 1, "stable", 0)

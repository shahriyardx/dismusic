from dataclasses import dataclass
from typing_extensions import Literal

__version__ = "1.1.1a2"


@dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(1, 1, 1, "alpha", 2)

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from setuptools import find_packages, setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Framework :: aiohttp",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

current_directory = Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

version_path = current_directory / "dismusic" / "_version.py"
module_spec = spec_from_file_location(version_path.name[:-3], version_path)
version_module = module_from_spec(module_spec)
module_spec.loader.exec_module(version_module)

setup(
    name="dismusic",
    version=version_module.__version__,
    description="Music cog for discord bots. Supports YouTube, YoutubeMusic, SoundCloud and Spotify.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shahriyardx/dismusic/",
    author="Md Shahriyar Alam",
    author_email="contact@shahriyar.dev",
    license="MIT",
    classifiers=classifiers,
    keywords="discord discord-music music-bot discord-music-bot lavalink wavelink",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=requirements,
    project_urls={
        "Bug Reports": "https://github.com/shahriyardx/dismusic/issues",
        "Source": "https://github.com/shahriyardx/dismusic/",
    },
)

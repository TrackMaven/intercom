from setuptools import find_packages, setup
import os

# Package meta-data.
NAME = "intercom"
DESCRIPTION = "A Python library fro the Intercom API."
URL = "https://github.com/TrackMaven/intercom"
EMAIL = "engineering@trackmaven.com"
AUTHOR = "TrackMaven Engineering"
VERSION = None
REQUIRED = ["requests==2.22.0"]

here = os.path.abspath(os.path.dirname(__file__))
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    include_package_data=True,
    install_requires=REQUIRED,
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    url=URL,
)

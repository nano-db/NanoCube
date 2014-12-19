from setuptools import setup, find_packages
from pip.req import parse_requirements
import os

def reqs():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    install_reqs = parse_requirements(req_path)
    return [str(ir.req) for ir in install_reqs]

setup(
    name="nanodb",
    version="0.1",
    license="Apache License 2.0",
    author="Pierre-Marie Dartus",
    author_email="dartus.pierremarie@gmail.com",
    url="https://github.com/pmdartus/NanoCube",
    description="In memory database for geolocated and temporal data",
    download_url="https://github.com/pmdartus/NanoCube/tarball/0.1",
    long_description=os.path.join(os.path.dirname(__file__), "Readme.md"),
    packages=find_packages(exclude=['test']),
    install_requires=reqs(),
    entry_points={
        "console_scripts": [
            "nanodb_server=libs.server:init_parser",
            "nanodb=libs.cli:init_parser"
        ]
    },
    include_package_data=True
)

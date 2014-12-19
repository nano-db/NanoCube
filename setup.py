from setuptools import setup, find_packages
from pip.req import parse_requirements
import os

def reqs():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    install_reqs = parse_requirements(req_path)
    return [str(ir.req) for ir in install_reqs]

setup(
    name="NanoDB",
    version="0.0.1",
    author="Pierre-Marie Dartus",
    author_email="dartus.pierremarie@gmail.com",
    url="https://github.com/pmdartus/NanoCube",
    description="In memory database for geolocated and temporal data",
    long_description=os.path.join(os.path.dirname(__file__), "Readme.md"),
    packages=find_packages(exclude=['test']),
    install_requires=reqs(),
    include_package_data=True
)

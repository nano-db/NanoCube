from setuptools import setup, find_packages

def readme():
    with open('README.rst') as readme:
        return readme.read()


setup(
    name="nanodb",
    version="0.4.2",
    license="Apache License 2.0",
    author="Pierre-Marie Dartus",
    author_email="dartus.pierremarie@gmail.com",
    url="https://github.com/pmdartus/NanoCube",
    description="In memory database for geolocated and temporal data",
    download_url="https://github.com/nano-db/NanoCube",
    long_description=readme(),
    packages=find_packages(exclude=['test']),
    install_requires=[
        "pyzmq>=14.4.1",
        "PyYAML==3.11",
        "nanodb_driver"
    ],
    entry_points={
        "console_scripts": [
            "nanodb_server=server.server:init_parser",
            "nanodb=client.cli:init_parser"
        ]
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
    ]
)

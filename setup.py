#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="xtables-monitor",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "Jinja2",
        "netifaces",
    ],
    scripts=[
        "bin/xtm",
    ],

    author="Frederik Möllers",
    author_email="frederik@die-sinlosen.de",
    description="Write firewall rules using templates",
    license="GPL3",
    url="https://github.com/frederikmoellers/xtables-monitor",
)

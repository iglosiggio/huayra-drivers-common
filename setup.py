#!/usr/bin/python3

from setuptools import setup

import subprocess, glob, os.path
import os
import sys

setup(
    name="huayra-drivers-common",
    author="Alberto Milone",
    author_email="albertomilone@alice.it",
    maintainer="Ignacio Losiggio",
    maintainer_email="iglosiggio@gmail.com",
    url="http://github.com/huayralinux",
    license="gpl",
    description="Detect and install additional Huayra driver packages",
    packages=["HuayraDrivers"],
    data_files=[("/usr/share/huayra-drivers-common/", ["share/fake-devices-wrapper"]),
                ("/var/lib/huayra-drivers-common/", []),
                ("/etc/", []),
                ("/usr/share/huayra-drivers-common/detect", glob.glob("detect-plugins/*")),
                ("/usr/share/doc/huayra-drivers-common", ['README.md']),
               ],
    scripts=["huayra-drivers"],
)

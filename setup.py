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
    packages=["Quirks", "UbuntuDrivers"],
    data_files=[("/usr/share/ubuntu-drivers-common/", ["share/fake-devices-wrapper"]),
                ("/var/lib/ubuntu-drivers-common/", []),
                ("/etc/", []),
                ("/usr/share/ubuntu-drivers-common/detect", glob.glob("detect-plugins/*")),
                ("/usr/share/doc/ubuntu-drivers-common", ['README']),
               ],
    scripts=["ubuntu-drivers"],
)

#!/usr/bin/env python

"""
Setup file for the Aurora plotting package: TOPAZ
"""
import os
import subprocess
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup_file = os.path.realpath(__file__)
data_dir = os.path.join(setup_file.rsplit("/", 1)[0], "data")

subprocess.run(["yt", "config", "set", "yt", "test_data_dir", data_dir])

setuptools.setup(
    name="topaz",
    version="0.0.7",
    author="Adam Batten",
    author_email="adamjbatten@gmail.com",
    description="A plotting package for the Aurora simulations using pynbody",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/abatten/topaz",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

setup(
    author="Hao-Ting Wang",
    author_email="htwangtw@gmail.com",
    python_requires=">=3.7",
    description="ADIE data curation tools",
    name="adie",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points="""
        [console_scripts]
        beh2bids=adie.scripts.beh2bids:main
    """,
    version="0.0.2",
)
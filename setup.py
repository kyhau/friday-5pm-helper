from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import os

# Makes setup work inside of a virtualenv
use_system_lib = True
if os.environ.get("BUILD_LIB") == "1":
    use_system_lib = False

base_dir = os.path.dirname(__file__)
__title__ = "friday_5pm_helper"
__version__ = "0.1.0.dev0"
__summary__ = "Friday 5pm helper."
__author__ = "Kay Hau"
__requirements__ = [
    'google-api-python-client>=1.5.4',
    'jira>=1.0.7'
]

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

entry_points = {
    'console_scripts': [
        'replicon-helper = friday_5pm_helper.replicon:main',
        'gcalendar-helper = friday_5pm_helper.gcalendar:main',
        'jira-helper = friday_5pm_helper.jira_checker:main',
    ]
}
setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    author=__author__,
    zip_safe=False,
    install_requires=__requirements__,
    entry_points=entry_points,
)

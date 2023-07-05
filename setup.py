from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in line/__init__.py
from line import __version__ as version

setup(
	name="line",
	version=version,
	description="A plugin that facilitates Line(platform) integration.",
	author="Muhammad Umer Farooq <github.com/umer2001>",
	author_email="umer2001.uf@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

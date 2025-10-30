import os
import re
import sys

from setuptools import find_packages, setup

if sys.argv[-1] == "publish":
	os.system("python setup.py sdist bdist_wheel")
	sys.exit()


def read(filename):
	with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
		return f.read()


version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', read('godm/__init__.py'), re.MULTILINE).group(1)

def get_requirements():
    with open("requirements.txt", encoding='utf-8') as f:
        return [r.strip("\n") for r in f.readlines()]

setup(
	name="godm",
	version=version,
	description="Data Object Model for Google Sheet",
	url="https://github.com/devendrapratap02/g-odm",
	author="Devendra Pratap Singh",
	author_email="dps.manit@gmail.com",
	keywords=["spreadsheets", "google-spreadsheets", "object-data-model"],
	install_requires=get_requirements(),
	python_requires=">=3.8",
	license="MIT",
	packages=find_packages(),
	zip_safe=False
)

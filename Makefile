#
#Make pymongo_aggregation
#
# Assumes passwords for pypi have already been configured with keyring.
#


PYPIUSERNAME="jdrumgoole"
ROOT=${HOME}/GIT/gdelttools

root:
	@echo "The project ROOT is '${ROOT}'"


python_bin:
	python -c "import os;print(os.environ.get('USERNAME'))"
	which python

prod_build:clean clean dist test
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u jdrumgoole

test_build: clean sdist test
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u jdrumgoole

#
# Just test that these scripts run
#
test_scripts:
	(export PYTHONPATH=`pwd` && python gdelttools/gdeltloader.py -h > /dev/null >&1)

test_all: nose test_scripts

nose:
	which python
	nosetests

dist:
	python setup.py bdist

sdist:
	python setup.py sdist

bdist_wheel:
	python setup.py bdist_wheel

test_install:
	pip install --extra-index-url=https://pypi.org/ -i https://test.pypi.org/simple/ pymongoimport

clean:
	rm -rf dist bdist sdist

pkgs:
	pipenv install pymongo keyring twine nose semvermanager

init: pkgs
	keyring set https://test.pypi.org/legacy/ ${USERNAME}
	keyring set https://upload.pypi.org/legacy/ ${USERNAME}

collect:
	python pymongoimport

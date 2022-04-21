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

build:
	python3 -m build

gitit:
	git add -u
	- git commit -m "Update for product build"
	git tag -a `python gdelttools\__version__.py` -m"Make file update"
	- git push

prod_build:clean gitit build
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u jdrumgoole

test_build: clean build
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

test_install:
	pip install --extra-index-url=https://pypi.org/ -i https://test.pypi.org/simple/ gdelttools

clean:
	rm -rf dist
	rm *.txt *.csv *.zip

pkgs:
	pipenv sync

init: pkgs
	keyring set https://test.pypi.org/legacy/ ${USERNAME}
	keyring set https://upload.pypi.org/legacy/ ${USERNAME}



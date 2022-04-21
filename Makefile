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
	git tag -a `python gdelttools/gdeltloader.py --version | cut -f2 -d' '` -m"Make file update"
	- git push

prod_build:clean gitit build
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u jdrumgoole

test_build: clean build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u jdrumgoole

#
# Just test that these scripts run
#
test_scripts: clean
	(export PYTHONPATH=`pwd` && python gdelttools/gdeltloader.py -h > /dev/null >&1)
	python gdelttools/gdeltloader.py --master
	python gdelttools/gdeltloader.py --master --download --last 1
	python gdelttools/gdeltloader.py --update
	python gdelttools/gdeltloader.py --update --download --last 1
	python gdelttools/gdeltloader.py --master --download --last 3
	python gdelttools/gdeltloader.py --master --overwrite
	python gdelttools/gdeltloader.py --master --download --last 1 --overwrite
	python gdelttools/gdeltloader.py --update --overwrite
	python gdelttools/gdeltloader.py --update --download --last 1 --overwrite
	python gdelttools/gdeltloader.py --master --download --last 3 --overwrite

test_all: nose test_scripts

nose:
	which python
	nosetests

test_install:
	pip install --extra-index-url=https://pypi.org/ -i https://test.pypi.org/simple/ gdelttools

clean:
	-rm -rf dist
	-rm *.txt *.CSV *.zip

pkgs:
	pipenv sync

init: pkgs
	keyring set https://test.pypi.org/legacy/ ${USERNAME}
	keyring set https://upload.pypi.org/legacy/ ${USERNAME}



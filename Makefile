#
#Make pymongo_aggregation
#
# Assumes passwords for pypi have already been configured with keyring.
#


PYPIUSERNAME="jdrumgoole"
ROOT=${HOME}/GIT/gdelttools

all: test_all build test_build
	-echo "Ace King, Check it out! A full build"

build:
	python3 -m build

gitit:
	git add -u
	- git commit -m "Update for product build"
	git tag -a `python gdelttools/gdeltloader.py --version | cut -f2 -d' '` -m"Make file update"
	- git push

reshape:
	mongosh --file=gdelt_reshaper.js

full_dataload:
	python gdelttools/gdeltloader.py --master --download
	sh mongoimport.sh
	mongosh --file=gdelt_reshaper.js

test_dataload:
	python gdelttools/gdeltloader.py --master --download --last 1
	sh mongoimport.sh
	mongosh --file=gdelt_reshaper.js

prod_build:clean gitit build
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u jdrumgoole

test_build: clean nose_test build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u jdrumgoole

#
# Just test that these scripts run
#
full_test: clean test_scripts clean
	echo "Full Test Complete"

nose_test: clean
	nosetests

test_scripts: clean
	(export PYTHONPATH=`pwd` && python gdelttools/gdeltloader.py -h > /dev/null >&1)
	python gdelttools/gdeltloader.py --master > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 1 > /dev/null
	python gdelttools/gdeltloader.py --update > /dev/null
	python gdelttools/gdeltloader.py --update --download --last 1 > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 3 > /dev/null
	python gdelttools/gdeltloader.py --master --overwrite > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 1 --overwrite > /dev/null
	python gdelttools/gdeltloader.py --update --overwrite > /dev/null
	python gdelttools/gdeltloader.py --update --download --last 1 --overwrite > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 3 --overwrite > /dev/null
	rm *.zip > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 3 > /dev/null
	rm *.CSV > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 3 > /dev/null
	rm *.CSV *.zip > /dev/null
	python gdelttools/gdeltloader.py --master --download --last 3 > /dev/null
	sh mongoimport.sh > /dev/null

test_all: clean nose_test test_dataload test_scripts
	-echo "Tests complete"


clean:
	-rm -rf dist
	-rm *.txt *.CSV *.zip

pkgs:
	pipenv sync

init: pkgs
	keyring set https://test.pypi.org/legacy/ ${USERNAME}
	keyring set https://upload.pypi.org/legacy/ ${USERNAME}



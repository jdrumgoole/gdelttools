

from setuptools import setup, find_packages
import os
import glob

pyfiles = [f for f in os.listdir(".") if f.endswith(".py")]

setup(
    name="gdelttools",
    version="0.01a",

    author="Joe Drumgoole",
    author_email="joe@joedrumgoole.com",
    description="gdelttools - tools to help with downloading GDELT data",
    long_description=
    '''
A set of tools to support downloading GDELT data. This includes downloading, unzipping and storing the meta data
''',

    license="AGPL",
    keywords="MongoDB GDELT",
    url="https://github.com/jdrumgoole/gdelttools",

    install_requires=['pymongo',
                      'requests'
                      'dnspython'
                    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7'],

    # setup_requires=["pymongo",
    #                   "nose",
    #                   "dnspython",
    #                   "dateutils",
    #                   "configargparse",
    #                   "toml"],

    packages=find_packages(),

    data_files=[("test", glob.glob("data/*.ff") +
                 glob.glob("data/*.csv") +
                 glob.glob("data/*.txt"))],
    python_requires='>3.7',
    scripts=[],
    entry_points={
        'console_scripts': [
            'gdeltloader=gdelttools.gdeltloader:main',
        ]
    },

    test_suite='nose.collector',
    tests_require=['nose'],
)



from setuptools import setup, find_packages
import os
import glob

pyfiles = [f for f in os.listdir(".") if f.endswith(".py")]

setup(
    name="gdelttools",
    version="0.04a1",

    author="Joe Drumgoole",
    author_email="joe@joedrumgoole.com",
    description="gdelttools - tools to help with downloading GDELT data",
    long_description=
    '''
A set of tools to support downloading GDELT data. This includes downloading, unzipping and storing the meta data
''',

    license="http://www.apache.org/licenses/LICENSE-2.0",
    keywords="MongoDB GDELT dataset",
    url="https://github.com/jdrumgoole/gdelttools",

    install_requires=['pymongo',
                      'requests',
                      'dnspython',
                    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

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

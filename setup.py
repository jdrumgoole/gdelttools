
from setuptools import setup, find_packages
import os
import glob


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSIONFILE="gdelttools/_version.py"
with open(VERSIONFILE, "rt") as vfile:
    for line in vfile:
        line = line.strip()
        (lhs, equals, rhs) = line.partition( "=")
        if lhs.strip() == "__version__":
            rhs = rhs.strip()
            version_string = rhs.strip('"')
pyfiles = [f for f in os.listdir(".") if f.endswith(".py")]


setup(
    name="gdelttools",
    version=version_string,

    author="Joe Drumgoole",
    author_email="joe@joedrumgoole.com",
    description="A set of tools to support downloading GDELT data",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache 2.0",
    keywords="MongoDB GDELT dataset",
    url="https://github.com/jdrumgoole/gdelttools",

    install_requires=['pymongo',
                      'requests',
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

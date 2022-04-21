import argparse
import pymongo

def main():

    parser = argparse.ArgumentParser(epilog=f"Version: {__version__}\n"
                                            f"More info : https://github.com/jdrumgoole/gdelttools ")

    parser.add_argument("--host",
                        help="MongoDB URI")

    client -m

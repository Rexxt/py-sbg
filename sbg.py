from argparse import ArgumentParser
import markdown as md
from rich import print

ap = ArgumentParser()
ap.add_argument('-f', '--folder', help='Folder to generate from', required=True)
ap.parse_args()

print(':page_facing_up:', 'SBG')
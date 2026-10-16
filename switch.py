#!/usr/bin/env python3
"""Switch the live overlay without focusing the transparent window."""
import argparse
from reticle import set_profile

parser = argparse.ArgumentParser(description="Change The Veil reticle profile")
parser.add_argument("mode", choices=("normal", "special", "toggle", "on", "off"))
args = parser.parse_args()
print(set_profile(args.mode))

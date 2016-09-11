#!/usr/bin/env python
# install_sourcemod.py
# Author: Jared Ballou
# Website: http://jballou.com/insurgency
import argparse
import sys
import os
from pprint import pprint

parser = argparse.ArgumentParser(description='Install MetaMod and SourceMod')

parser.add_argument("--platform", type=str, default="linux", help='')
parser.add_argument("--addons_path", type=str, default=os.getcwd(), help='')
parser.add_argument("--cachedir", type=str, default="/tmp", help='')
parser.add_argument("--githubuser", type=str, default="jaredballou", help='')
parser.add_argument("--githubrepo", type=str, default="linuxgsm", help='')
parser.add_argument("--githubbranch", type=str, default="master", help='')
parser.add_argument("--mm_path", type=str, default="%(addons_path)s/metamod", help='')
parser.add_argument("--mm_url_base", type=str, default="http://www.sourcemm.net/downloads/", help='')
parser.add_argument("--mm_file_latest", type=str, default="", help='')
#$(curl -sL "%(mm_url_base)s" | grep -m1 -o "mmsource-[0-9\.a-zA-Z]*-linux\.tar\.gz")
parser.add_argument("--sm_major_version", type=str, default="1.7", help='')
parser.add_argument("--sm_url_base", type=str, default="http://www.sourcemod.net/smdrop/%(sm_major_version)s/", help='')
parser.add_argument("--sm_url_latest", type=str, default="%(sm_url_base)ssourcemod-latest-%(platform)s", help='')
parser.add_argument("--sm_file_latest", type=str, default="%(sm_url_latest)s", help='')
#"$(curl -sL "${sm_url_latest}")"
parser.add_argument("--sm_url_file", type=str, default="%(sm_url_base)s%(sm_file_latest)s", help='')
parser.add_argument("--sm_file", type=str, default="%(cachedir)s/%(sm_file_latest)s", help='')

#{k: v % vars(args) for k, v in vars(args).iteritems()}
#opts = vars(args)
#.keys())
# This downloads and installs the latest stable versions of MetaMod and SourceMod
def main():
	args = parser.parse_args()
	opts = interpolate(data=vars(args))
	pprint(opts)
	install_metamod()
	install_sourcemod()

def install_metamod():
	print "Install MetaMod"
def install_sourcemod():
	print "Install SourceMod"

def interpolate(key=None, data=None, interpolate_data=None):
	val = ""
	if data is None:
		data = vars(args)
	if interpolate_data is None:
		interpolate_data = data

	if key is None:
		item = data
	else:
		if not key in data.keys():
			return
		item = data[key]

	kt = type(item)
	if kt in [str, int]:
		val = item
	if kt in [list]:
		val = ', '.join(map(str, item))
	if kt in [set,tuple]:
		val = item.join(", ")
	if kt in [dict]:
		vals = dict()
		for skey in item.keys():
			vals[skey] = interpolate(key=skey,data=item,interpolate_data=interpolate_data)
		return vals
	try:
		while (val.find('%') != -1):
			val = (val) % interpolate_data
	except:
		return val
	return val

if __name__ == "__main__":
	main()

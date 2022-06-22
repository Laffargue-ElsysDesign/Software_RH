#!/bin/bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ -z "$PYNQ_OVERLAYS_REMOTE_PREFIX" ]]; then
	PYNQ_OVERLAYS_REMOTE_PREFIX="https://www.xilinx.com/bin/public/openDownload?filename=pynq."
fi

usage () {
echo "$0" >&2
echo "" >&2
echo "Script for building default overlays, microblaze bsp's and binaries." >&2
echo "" >&2
}

checkdeps () {
for f in vivado vitis curl; do
	if ! which $f > /dev/null; then
		echo "Could not find command $f, please ensure it is installed" 2>&1
		exit 1
	fi
done
}

# bitstream building will be skipped only if bit and hwh are both available
build_bitstreams () {
	local root=$1
	local board=$2
	local orig_dir=$(pwd)
	cd $root/$board
	local overlays=`find . -maxdepth 2 -iname 'makefile' | cut -f2 -d"/"`
	for ol in $overlays ; do
		cd $root/$board/$ol
		if [[ -e $ol.bit && -e $ol.hwh ]]; then
			echo "skipping bitstream $ol.bit for $board"
		else
			echo "building bitstream $ol.bit for $board"
			make clean && make
		fi
	done
	cd $orig_dir
}

get_opendownloads_file() {
    local remote_file=$1
    local local_file=$2

    curl -L -s $remote_file --output $local_file 2>/dev/null
    ftype=$(file $local_file | awk '{print $2}')

    # if opendownloads returns an HTML type, then most likely a 404 page...
    # TODO: something cleaner, but for now, remove the file like it never arrived
    if [ "$ftype" = "HTML" ]; then
	rm $local_file
    fi
    
}

get_bitstreams () {
	local root=$1
	local board=$2
	local orig_dir=$(pwd)
	cd $root/$board
	local overlays=`find . -maxdepth 2 -iname 'makefile' | cut -f2 -d"/"`
	for ol in $overlays ; do
		cd $root/$board/$ol
		tcl_md5=$(md5sum $ol.tcl | awk '{print $1}')
		if [ ! -e $ol.bit ] || [ ! -e $ol.hwh ]; then
			rm -f $ol.bit $ol.hwh
			set +e
			get_opendownloads_file ${PYNQ_OVERLAYS_REMOTE_PREFIX}$board.$ol.$tcl_md5.bit $ol.bit
			get_opendownloads_file ${PYNQ_OVERLAYS_REMOTE_PREFIX}$board.$ol.$tcl_md5.hwh $ol.hwh
			set -e
			if [ ! -s $ol.bit ] || [ ! -s $ol.hwh ] || [ ! -e $ol.bit ] || [ ! -e $ol.hwh ]; then
				# download failed for .bit, .hwh, or both. 
				# Cleanup to avoid potential issues later
				rm -f $ol.bit
				rm -f $ol.hwh
			fi
		fi
		if [ ! -e $ol.xsa ]; then
			set +e
			get_opendownloads_file ${PYNQ_OVERLAYS_REMOTE_PREFIX}$board.$ol.$tcl_md5.xsa $ol.xsa
			set -e
			if [ ! -s $ol.xsa ] || [ ! -e $ol.xsa ]; then
				rm -f $ol.xsa
			fi
		fi
	done
	cd $orig_dir
}

usage
checkdeps

cd $script_dir/boards
boards=`find . -maxdepth 2 -name '*.spec' -printf '%h\n' | cut -f2 -d"/"`
for b in $boards ; do
	get_bitstreams "$script_dir/boards" "$b"
done

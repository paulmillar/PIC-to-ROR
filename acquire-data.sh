#!/bin/bash
#
#  Script for downloading CORDIS data
#
set -e

basedir="$(cd $(dirname $0);pwd)"

function fail {
    echo "$2"
    exit $1
}

function download { # $1 - URL, $2 - file, $3 - checksum
    mkdir -p $CACHE

    local url="$1"
    local default_file=
    local file=${2:-${url##*/}}

    if [ -f $CACHE/$file ]; then
	if [ "$3" != "" ]; then
	    expected=${3#md5:}
	    actual=$(md5sum $CACHE/$file|cut -d" " -f1)
	    if [ "$expected" = "$actual" ]; then
		echo "Cached file $file matches expected checksum; not downloading"
		return
	    else
		echo "Checksum mismatch ($actual != $expected)"
	    fi
	fi
	check_modified="-z $file"
	echo "Checking for updates in $url"
    else
	echo "Downloading $url as $file"
    fi

    (cd $CACHE; curl $check_modified -# -o "$file" $url)
}


TARGET=data

mkdir -p "$TARGET"
cd "$TARGET"
rm -f *.csv *.json

echo
echo Acquiring CORDIS data
echo

CACHE=cache
REF=reference

UNZIP="unzip -q -o"

download https://cordis.europa.eu/data/cordis-h2020projects-csv.zip
$UNZIP $CACHE/cordis-h2020projects-csv.zip
mv csv/* .
rmdir csv

echo
echo Acquiring ROR data
echo

metadata_url='https://zenodo.org/api/records/?communities=ror-data&sort=mostrecent'
download "$metadata_url" ror-metadata

checksum=$(jq -r '.hits.hits[0].files[0].checksum' $CACHE/ror-metadata)
zip_url=$(jq -r '.hits.hits[0].files[0].links.self' $CACHE/ror-metadata)
key=$(jq -r '.hits.hits[0].files[0].key' $CACHE/ror-metadata)

download $zip_url $key $checksum
$UNZIP $CACHE/$key
mv *-ror-data.json ror-data.json


#python3 "$basedir/process.py" organization.csv > organizations.json

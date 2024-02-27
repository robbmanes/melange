#!/bin/bash

# Finds the current file locks in the desired path, with exclusions.
find_file_locks() {
	SEARCHDIR="/var/lib/containers"
	echo "Finding file locks in the ${SEARCHDIR} path..."
	find "${SEARCHDIR}" -type f \
		\( \
			-not -path "*/storage/overlay/*" \
			-not -path "*/storage/overlay-images/*" \
			-not -path "*/storage/overlay-layers/*" \
			-not -path "*/storage/volumes/*" \
		\) \
	| xargs fuser
}

find_file_locks

#!/bin/bash

# Print full information for every shared memory segment; useful for finding lock holders
report_ipcs_shmem() {
	echo "Checking every shared memory segment and their current owners..."
	echo "======================================================"
	ipcs -m
	for SHMID in $(ipcs -m | awk '/[0-9]/ {print $2}')
	do
		ipcs -m -i $SHMID
	done
	echo "======================================================"
}

report_ipcs_shmem

#!/bin/bash

# Find all processes being ptraced, report the tracer and tracee.
find_all_ptraces() {
        echo "Finding all ptraced processes..."
	TRACE_FOUND=0
        for PID in $(ls /proc/ | egrep [0-9])
        do
                TRACER=$(awk '/TracerPid/ {print $2}' /proc/$PID/status 2>/dev/null)

                if [ ! -z "${TRACER}" ]  && [ "${TRACER}" -ne 0 ];
                then
			TRACE_FOUND=1
                        COMM_TRACEE=$(cat /proc/$PID/comm)
                        COMM_TRACER=$(cat /proc/$TRACER/comm)
                        echo "Process ${PID} (${COMM_TRACEE}) is being ptraced by ${TRACER} (${COMM_TRACER})"
                fi
        done
	if [ "$TRACE_FOUND" != 1 ]
	then
		echo "No ptraced processes found."
	fi
}

find_all_ptraces

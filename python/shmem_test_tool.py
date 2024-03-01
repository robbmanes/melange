#!/usr/bin/env python

import sys
import time


def usage():
    msg = '''
shmem_test_tool.py
==================
Utility for testing Python multiprocessing shared memory segments.
Note this is NOT the same as IPCS SHMEM segments in Linux/Unix.

Usage:
    - Run with no arguments to create a shared memory segment.
        # shmem_test_tool.py

    - Run with the name of a shared memory segment to attach to that segment.
        # shmem_test_tool.py [SHMEM_NAME]

*Requires python 3.8 or higher to run.*
'''
    print(msg)

# Only python3.8+ has shared_memory, only load on-demand.
def shmem_import():
    try:
        global shared_memory
        from multiprocessing import shared_memory
    except Exception as e:
        print("Failed to import multiprocessing.shared_memory: %s" % e)
        sys.exit(-1)

# Make sure we're on python3.8 or higher.
def check_python_version():
    curr_version = str(sys.version_info.major) + '.' + str(sys.version_info.minor)
    err_msg = '''
Current detected Python version is %s

This tool *must* be run with Python 3.8 or higher to allow for shared memory access.

Please re-run this tool with the appropriate Python binary.'''

    if float(curr_version) < 3.8:
        print(err_msg % curr_version)
        sys.exit(-1)

# Execution begins here.
def main():
    check_python_version()
    shmem_import()

    if len(sys.argv) == 1:
        # If there are no arguments detected, assume we're just going to make a new shared memory segment.
        print("No arguments detected - creating new shared memory segment.")
        try:
            print("Creating shared memory segment...")
            shm = shared_memory.SharedMemory(create=True, size=0xf)
            print("Shared memory segment \"%s\" created." % shm.name)
        except Exception as e:
            print("Error during shared memory creation: %s" % e)
            return -1

        print("Shared memory segment should be created - sleeping until Ctrl-C is issued.")
        while True:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                print("KeyboardInterrupt detected, closing shared memory segments and exiting.")
                try:
                    shm.close()
                    shm.unlink()
                except Exception as e:
                    print("Unable to close shared memory segment: %s" % e)
                    sys.exit(-1)
                sys.exit(0)
    elif len(sys.argv) == 2:
        # If an argument is supplied, assume it is the shared memory segment name and try to attach.
        shm_name = sys.argv[1]
        print("Attempting to attach to shared memory segment \"%s\"..." % shm_name)
        try:
            shm = shared_memory.SharedMemory(name=shm_name, create=False)
        except Exception as e:
            print("Unable to utilize shared memory segment \"%s\": %s" % (shm_name, e))
            sys.exit(-1)

        print("Successfully attached to shared memory segment \"%s\". Sleeping until Ctrl-C is issued." % shm_name)
        while True:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                try:
                    shm.close()
                except Exception as e:
                    print("Unable to close shared memory segment: %s" % e)
                    sys.exit(-1)
                sys.exit(0)
    else:
        usage()
        sys.exit(-1)

if __name__ == '__main__':
    sys.exit(main())

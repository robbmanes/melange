# bash
`bash` shell scripts I've authored over time provided in the hopes they'll be useful in the future.

## index
- `find_all_ptraces.sh`: locates all processes marked as being `ptraced` and reports who is tracing them.
- `report_ipcs_shmem.sh`: print full information for every shared memory segment; useful for finding lock holders
- `find_file_locks.sh`: finds current file locks in the desired path, with exclusions; requires changing the `SEARCHDIR` variable prior to running.
- `buildah-support-tools-infiniband.sh`: uses `buildah` to build infiniband support into the base RHEL support-tools image; useful as a `buildah` example script

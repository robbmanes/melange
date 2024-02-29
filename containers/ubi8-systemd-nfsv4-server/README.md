# ubi8-systemd-nfsv4-server
Container image to run an `nfsv4` server under a systemd unit.

## build
```
# podman build -f Dockerfile -t localhost/ubi8-systemd-nfsv4-server .
```

## run
```
# podman run -itd --name nfsv4-server --privileged --systemd=true -v NFSvol:/mnt/test_shares:Z localhost/ubi8-systemd-nfsv4-server
```

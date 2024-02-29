# rhel9-systemd-postfix
postfix running on ubi9 underneath systemd; requires Red Hat subscription to build as it uses non-UBI packages.

## build
```
$ podman build -t localhost/systemd-postfix .
```

## deploy
```
$ podman run -itd --name postfix -p 25:25 localhost/systemd-postfix
```

# zombie-probe
Container image with built-in probe intentionally made to show that execs that do not call `wait()` syscalls on their child processes.

Do not run for any reason.  This software will cause detrimental behaviors in your environments *intentionally*.  It has been created to reproduce a specific scenario, notably creation of zombie processes when using a TTY and subprocesses.

## usage
You can simulate this in either a local container engine or using Kubernetes/OpenShift.

The image is available at `quay.io/robbmanes/zombie_probe:latest` for pulling:
```
$ podman pull quay.io/robbmanes/zombie_probe:latest
```

If you want to build it locally, you can do so via:
```
$ podman built -t quay.io/robbmanes/zombie_probe:latest .
```

### podman/docker
Using a local container engine, run an infinite `sleep` process as PID 1, simulating a normal application:
```
$ podman run -d --name test-zombies quay.io/robbmanes/zombie_probe:latest sleep infinity
```

After the container is running, you can generate zombified `sleep` processes by running the in-container-image script as an `exec`:
```
$ podman exec -it --name test-zombies sh -c 'python3.11 zombie_probe.py'
```

Note that using `-it` is necessary over `-d`, as a TTY must be present for the zombie process to appear:
```
$ ps aux | grep sleep
101000    171658  0.0  0.0   7868  1352 ?        Ss   09:45   0:00 /usr/bin/coreutils --coreutils-prog-shebang=sleep /usr/bin/sleep infinity
101000    171722  0.0  0.0      0     0 ?        Z    09:46   0:00 [sleep] <defunct>
```
The first process is the entrypoint of the container (`--coreutils-prog-shebang`) calling `sleep infinity` and the second defunct entry is our now-zombified `exec` of a python script that creates a defunct `sleep` process.  Any process that exits *after* the `Popen` within the python script can be used.

### Kubernetes/OpenShift
Run the provided `pod.yml` configuration to create a zombie-pod:
```
$ oc create -f pod.yml
pod/zombie-exec-pod created

$ oc get pod zombie-exec-pod
NAME              READY   STATUS    RESTARTS   AGE
zombie-exec-pod   1/1     Running   0          52s
```

Observe as, using the `exec` method as a `livenessProbe` that does not properly call `wait` on its child processes, `sleep` defunct processes build up over time:
```
$ oc rsh zombie-exec-pod

(app-root) sh-5.1$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
default        1  0.0  0.0   7868  1348 ?        Ss   14:21   0:00 /usr/bin/coreutils --coreutils-prog-shebang=sleep /usr/bin/sleep infini
default       13  0.0  0.0      0     0 ?        Z    14:23   0:00 [sleep] <defunct>
default       20  0.0  0.0      0     0 ?        Z    14:24   0:00 [sleep] <defunct>
default       27  0.0  0.0      0     0 ?        Z    14:25   0:00 [sleep] <defunct>
default       34  0.0  0.0   7868  1348 ?        S    14:26   0:00 /usr/bin/coreutils --coreutils-prog-shebang=sleep /usr/bin/sleep 60
default       35  0.6  0.0   7388  4036 pts/0    Ss   14:26   0:00 /bin/sh
default       42  0.0  0.0  10084  3576 pts/0    R+   14:26   0:00 ps aux
```

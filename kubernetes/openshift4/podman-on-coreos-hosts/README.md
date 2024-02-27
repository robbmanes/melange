# podman-on-coreos-hosts
Object definitions for setting CoreOS nodes in OpenShift Container Platform 4 to host a Podman API UNIX socket (Emulating Docker-Engine API and/or Docker-Compose API) and example job that mounts the socket from the host.

Primarily useful for older Jenkins `withDockerContainer` or `gradle` deployments that need to deploy from Docker based k8s (OpenShift 3) to OpenShift 4.

This is *very very insecure* and *not recommended to ever run*.  You are giving your Jobs full access to the host carte-blanche.  It really should only be ever used as a stopgap to a properly scoped CI/CD system that operates in pods and doesn't require host-level access to a container engine/runtime.  **USE AT YOUR OWN RISK**.

## deploy
- Deploy the objects to your cluster.
```
$ oc create -f podman-on-coreos-hosts.yaml
namespace/podman-api-host created
serviceaccount/podman-api-host created
securitycontextconstraints.security.openshift.io/podman-api-host created
machineconfig.machineconfiguration.openshift.io/99-podman-api-socket created
```
- Label the nodes you want to serve the `podman` API UNIX socket on.  This will cause the node to be deployed with an updated `MachineConfig` which will reboot that node.
```
$ oc label node/worker-0.example.com podman-api-host=true
node/worker-0.example.com labeled
```
- Deploy the test job to ensure it's working properly:
```
$ oc create -f podman-on-coreos-hosts-test.yaml

$ oc project podman-api-host
Now using project "podman-api-host" on server "https://mycluster.example.com:6443".

$ oc get pods
NAME                         READY   STATUS              RESTARTS   AGE
podman-api-host-test-vdnlh   0/1     ContainerCreating   0          44s

$ oc logs podman-api-host-test-vdnlh
time="2024-02-27T15:42:28Z" level=info msg="podman filtering at log level debug"
time="2024-02-27T15:42:28Z" level=debug msg="Called ps.PersistentPreRunE(podman --log-level=debug --remote --url unix:/var/run/docker.sock ps -a)"
time="2024-02-27T15:42:28Z" level=debug msg="DoRequest Method: GET URI: http://d/v4.6.1/libpod/_ping"
time="2024-02-27T15:42:28Z" level=debug msg="DoRequest Method: GET URI: http://d/v4.6.1/libpod/_ping"
time="2024-02-27T15:42:28Z" level=debug msg="DoRequest Method: GET URI: http://d/v4.6.1/libpod/containers/json"
CONTAINER ID  IMAGE                                                                                                                   COMMAND               CREATED       STATUS      PORTS       NAMES
58d2f46b5985  quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:b0d1a63c79f14392d467c26dab6b580d9877cfb552901593b13491edf1787130  firstboot-complet...  25 hours ago  Created                 stupefied_panini
time="2024-02-27T15:42:28Z" level=debug msg="Called ps.PersistentPostRunE(podman --log-level=debug --remote --url unix:/var/run/docker.sock ps -a)"
time="2024-02-27T15:42:28Z" level=debug msg="Shutting down engines"
```
- Pods can now be run in a similar fashion to the `Job` present in `podman-on-coreos-hosts-test.yaml`, using `spc_t` and `hostPath` mounts for the UNIX socket, to pass the "Docker" socket into the pod.

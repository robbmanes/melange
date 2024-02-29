FROM registry.access.redhat.com/ubi8/ubi:latest

USER root

# config
RUN echo 'RPCNFSDARGS=""\n\
RPCNFSDARGS=""\n\
RPCNFSDCOUNT=${RPCNFSDCOUNT}\n\
RPCMOUNTDOPTS=""\n\
STATDARG=""\n\
SMNOTIFYARGS=""\n\
RPCIDMAPDARGS=""\n\
RPCGSSDARGS=""\n\
GSS_USE_PROXY="yes"\n\
BLKMAPDARGS=""\n'\
>> /etc/sysconfig/nfs

EXPOSE  111 662 875 892 2049 45209 58329 443 139 445

# systemd
RUN yum install -y nfs-utils sysstat procps-ng xfsprogs; \
    (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
    systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*;\
    rm -f /etc/systemd/system/*.wants/*;\
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*; \
    rm -f /lib/systemd/system/anaconda.target.wants/*; \

    systemctl enable nfs-server; \
    mkdir -p /mnt/test_shares/; \
    echo "/mnt/ *(ro,no_root_squash,fsid=0)" >> /etc/exports.d/nfs.exports; \
    echo "/mnt/test_shares/ *(rw)" >> /etc/exports.d/nfs.exports; \

    rm -rf /pkg; rm -rf /tmp/*;

RUN rm -v /etc/system-fips

ENV container docker
STOPSIGNAL SIGRTMIN+3
# CMD ["/usr/sbin/init"]
CMD ["/usr/sbin/init", "--log-target=console", "--default-standard-output=journal+console"]

FROM registry.access.redhat.com/ubi9-init:latest
USER root
RUN yum install postfix -y && \
    yum clean all && \
    systemctl enable postfix
EXPOSE 25
CMD ["/sbin/init"]

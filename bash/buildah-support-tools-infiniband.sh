#!/bin/bash

# Builds infiniband support into the base RHEL support-tools image.
# Must be run from a subscribed RHEL host that has "buildah" installed.

IMAGE_NAME="quay.io/robbmanes/support-tools-ib:latest"

function main() {
        echo "Pulling latest support-tools container image..."
        CONTAINER=$(buildah from registry.redhat.io/rhel8/support-tools)
        echo "Made working container \"$CONTAINER\"."
        echo "Installing Infiniband support..."
        buildah run $CONTAINER /usr/bin/yum install infiniband-diags libibverbs libibverbs-utils -y
        echo "Committing container \"$CONTAINER\" to image \"$IMAGE_NAME\"."
        buildah commit $CONTAINER $IMAGE_NAME
        echo "Pushing image..."
        buildah push $IMAGE_NAME
        echo "Image should have finished pushing.  Run the image with:"
        echo "     $ podman container runlabel RUN $IMAGE_NAME"
}

main

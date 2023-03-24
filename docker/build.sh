#!/bin/bash
pushd $(dirname $0)/..
repo=ghcr.io
namespace=trellis-logic
image_name=ntcip-relay-server
tag=1.1
buildargs=
if [[ "$@" != *"--push"* ]]; then
    buildargs="$buildargs --output=type=docker"
fi
docker buildx build ${buildargs} -f docker/Dockerfile -t ${repo}/${namespace}/${image_name}:${tag} $@ .

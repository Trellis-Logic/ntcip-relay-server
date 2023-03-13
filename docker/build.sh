#!/bin/bash
pushd $(dirname $0)/..
repo=ghcr.io
namespace=trellis-logic
image_name=ntcip-relay-server
tag=1.0
docker buildx build --platform linux/arm64/v8 --platform linux/amd64 -f docker/Dockerfile -t ${repo}/${namespace}/${image_name}:${tag} $@ .

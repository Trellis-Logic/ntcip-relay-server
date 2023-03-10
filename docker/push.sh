#!/bin/bash
echo "See https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry"
echo "Please login using"
echo "export CR_PAT=YOUR_TOKEN"
echo "echo \$CR_PAT | docker login ghcr.io -u USERNAME --password-stdin"
echo "before calling this script"
namespace=trellis-logic
repo=ghcr.io
image_name=ntcip-relay-server
docker tag ${image_name} ${repo}/${namespace}/${image_name}
docker push ${repo}/${namespace}/${image_name}


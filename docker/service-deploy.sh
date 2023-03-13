#!/bin/bash
echo "Deploy service to Sighthound services repo"
scriptdir=$(realpath $(dirname $0))
pushd $(dirname $0)/..
if [ ! -e ../services ]; then
    echo "Expected a \"services\" directory or symlink at $(realpath $(pwd)/..)"
fi
cp -r ${scriptdir}/service ../services/ntcip-relay-server

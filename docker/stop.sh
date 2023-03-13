#!/bin/bash
pushd $(dirname $0)/service
docker-compose down

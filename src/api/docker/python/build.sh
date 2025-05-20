#!/usr/bin/env bash

# Remove Old Image
docker rm -f fastapi-docker

# No Cache Build
docker build --no-cache -t fastapi-docker -f docker/python/Dockerfile .
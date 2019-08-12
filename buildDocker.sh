#!/bin/bash
imageName=freecad-dev:latest
containerName=freecad-dev

docker build -t $imageName -f Dockerfile  .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
docker run -it --mount type=bind,source=$PWD,target=/app --name $containerName $imageName

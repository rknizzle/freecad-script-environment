# Dockerfile that creates a Ubuntu container with FreeCAD installed
FROM ubuntu:18.04

# Skips the time zone selection when installing FreeCAD
# Requires user interaction otherwise
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y software-properties-common
# Add freecad-maintainers personal package archive
RUN add-apt-repository -y ppa:freecad-maintainers/freecad-stable

# install freecad from PPA
RUN apt-get install -y freecad
# install python3-pip if python3 dependencies are needed
#RUN apt-get install -y pip3

# Quickfix: Create file links -- shouldn't be needed in future FreeCAD updates
RUN ln -s /usr/lib/freecad/Mod /usr/lib/freecad-python3/Mod
RUN ln -s /usr/lib/freecad/Ext /usr/lib/freecad-python3/Ext

# copy scripts to Docker image
COPY . /app

WORKDIR /app

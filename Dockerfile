FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install sudo openjdk-19-jre-headless
RUN mkdir -p /minecraft
RUN useradd -u 1000 -ms /bin/bash minecraft
WORKDIR /minecraft
RUN  echo "minecraft ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER 1000
ENV PATH=/minecraft/.local/bin:$PATH
ENV HOME=/minecraft
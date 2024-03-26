FROM ubuntu:22.04
RUN apt-get update
RUN apt-get -qq -y install curl wget unzip zip perl bzip2 cpanminus
RUN apt-get install -y openjdk-8-jdk
RUN apt-get install -y openjdk-8-jre
RUN update-alternatives --config java
RUN update-alternatives --config javac
RUN apt-get install -y python3 git
RUN mkdir defects4j_mf
WORKDIR defects4j_mf
COPY defects4j_multi_with_jars.patch defects4j_multi_with_jars.patch
COPY setup.py setup.py
COPY fault_data/ fault_data/

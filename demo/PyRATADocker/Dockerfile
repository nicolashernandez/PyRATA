FROM ubuntu:16.04
MAINTAINER Nicolas Hernandez < nicolas.hernandez [ at ] gmail.com >

RUN echo deb http://downloads.skewed.de/apt/xenial xenial universe > /etc/apt/sources.list.d/my_xenial.list
RUN echo deb-src http://downloads.skewed.de/apt/xenial xenial universe >> /etc/apt/sources.list.d/my_xenial.list

RUN apt-get update \
&& apt-get install -y python3 \
&& apt-get install -y python3-pip \
# demo pyrata_re.py
&& apt-get install -y --allow-unauthenticated python3-graph-tool \
&& apt-get install -y python3-nltk \
&& apt-get install -y evince \
# brown, punkt...
&& python3 -m nltk.downloader all \
&& apt-get install -y wget \
&& rm -rf /var/lib/apt/lists/*

RUN pip3 install pyrata
RUN wget  -P /root https://raw.githubusercontent.com/nicolashernandez/PyRATA/master/pyrata_re.py
FROM python:2

RUN wget https://github.com/jgm/pandoc/releases/download/2.3/pandoc-2.3-1-amd64.deb -O pandoc.deb \
         --progress=dot:giga
RUN dpkg -i pandoc.deb
RUN pip install bs4 pypandoc requests

COPY . /book/
WORKDIR /book

ENTRYPOINT make

FROM python:3.8-slim-buster

ARG UNAME=pydanticuser
ARG UID=1000
ARG GID=1000
ARG PYDANTIC_VERSION=1.7.3
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

RUN pip3 install pytest
RUN pip3 install pydantic==${PYDANTIC_VERSION}

COPY . .

USER $UNAME

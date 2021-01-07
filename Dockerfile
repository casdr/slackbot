FROM docker.mijn.breedband.nl/rd/docker/debian:buster

LABEL authors="Cas de Reuver <cas@reuver.co>"

EXPOSE 3000

ENV TZ="Europe/Amsterdam"

ADD ./docker_deps/services.d /etc/services.d
ADD . /app

RUN echo "** ensure timezone is set to $TZ **" && \
		ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN echo "** ensure apt-cache is updated **" && \
		apt-get update

RUN echo "** ensure python is installed **" && \
		apt-get install -y python3 python3-pip

RUN echo "** ensure pipenv is installed **" && \
		pip3 install pipenv

RUN echo "** ensure dependencies are isntalled **" && \
		cd /app && pipenv install

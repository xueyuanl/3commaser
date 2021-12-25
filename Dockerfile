FROM ubuntu:20.04
COPY ./requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y \
	python3-pip \
	vim && pip install -r ./requirements.txt 

COPY ./commasapi ./commasapi
COPY ./commaser ./commaser
COPY ./futures ./futures
COPY ./constants.py ./log.py ./update.py ./harmonic_trade.py ./

EXPOSE 3333

# ENTRYPOINT ["/bin/bash"]

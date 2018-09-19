FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y lsb-release gnupg curl && \
    export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s` && \
    echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y openssh-server python-pip gcsfuse rsyslog && \
    apt-get -y clean

RUN addgroup --gid 9000 sftp-users

RUN mkdir -p /var/run/pipes/ && \
    mkdir -p /etc/ssh/authorized-keys && \
    mkdir -p /run/sshd && \
    mkdir -p /var/landing/dev && \
    mkdir -p /var/landing/stage && \
    mkdir -p /var/run/sshd  && \
    mkfifo /var/run/pipes/consolidated && \
    chown syslog:adm /var/run/pipes/consolidated && \
    rm -rf /var/log/*

ADD ./image/ /

RUN pip install --upgrade pip
RUN pip install -r /opt/build/requirements.txt

ENV PYTHONPATH /opt/build/

EXPOSE 22

CMD /opt/run.sh

FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y lsb-release gnupg curl && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y openssh-server python-pip rsyslog google-cloud-sdk && \
    apt-get -y clean

RUN addgroup --gid 9000 sftp-users

RUN mkdir -p /var/run/pipes/ && \
    mkdir -p /etc/ssh/authorized-keys && \
    mkdir -p /run/sshd && \
    mkdir -p /var/landing/dev && \
    mkdir -p /var/landing/stage/ingest && \
    mkdir -p /var/landing/stage/error && \
    mkdir -p /var/landing/stage/log && \
    mkdir -p /var/staging && \
    mkdir -p /var/run/sshd  && \
    mkdir -p /var/secrets/credentials && \
    mkdir -p /var/secrets/ssh_host_keys && touch /var/secrets/ssh_host_keys/_holder && \
    mkfifo /var/run/pipes/consolidated && \
    chown syslog:adm /var/run/pipes/consolidated && \
    rm -rf /var/log/*

ADD ./image/ /

RUN pip install --upgrade pip
RUN pip install -r /opt/build/requirements.txt

ENV PYTHONPATH /opt/build/

CMD /opt/run.sh

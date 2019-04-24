FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y lsb-release gnupg curl && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y openssh-server python-pip rsyslog google-cloud-sdk vim && \
    apt-get -y clean


ARG APP_SFTP_GUID
ARG APP_SFTP_AUTHORIZEDKEYS_DIR
ARG APP_LANDING_DIR
ARG APP_PIPE_DIR
ARG APP_RAW_LOG_PIPE
ARG APP_LANDING_DEV_DIR

RUN addgroup --gid $APP_SFTP_GUID sftp-users

RUN mkdir -p $APP_PIPE_DIR && \
    mkdir -p $APP_SFTP_AUTHORIZEDKEYS_DIR && \
    mkdir -p /run/sshd && \
    mkdir -p $APP_LANDING_DIR && \
    mkdir -p /var/run/sshd  && \
    mkfifo $APP_RAW_LOG_PIPE && chown syslog:adm $APP_RAW_LOG_PIPE && \
    rm -rf /var/log/*

ADD ./src/opt/requirements.txt /opt/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /opt/requirements.txt

ENV PYTHONPATH /opt/app/

ADD ./src/ /

CMD python /opt/app/bin/launch.py

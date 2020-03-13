FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y lsb-release gnupg curl && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y openssh-server python-pip python3-pip rsyslog google-cloud-sdk vim jq locales && \
    apt-get -y clean


ARG APP_SFTP_GUID
ARG APP_SFTP_AUTHORIZEDKEYS_DIR

RUN addgroup --gid $APP_SFTP_GUID sftp-users

RUN mkdir -p $APP_SFTP_AUTHORIZEDKEYS_DIR && \
    mkdir -p /run/sshd && \
    mkdir -p /var/run/sshd

RUN echo "*.* /var/log/sshd/sshd.log" >> /etc/syslog.conf

RUN dbus-uuidgen > /var/lib/dbus/machine-id
RUN mkdir -p /var/run/dbus
RUN dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address

ADD ./src/opt/requirements.txt /opt/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/requirements.txt

ENV PYTHONPATH /opt/app/

ADD ./src/ /

CMD python3 /opt/app/bin/launch.py

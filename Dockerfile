FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y lsb-release gnupg curl && \
    apt-get update && \
    apt-get install -y openssh-server python-pip python3-pip rsyslog vim jq locales && \
    apt-get -y clean


RUN addgroup --gid 9000 sftp-users

RUN mkdir -p /etc/ssh/authorized-keys && \
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

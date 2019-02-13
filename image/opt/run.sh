#! /bin/bash

python /opt/build/bin/setup.py 2>&1

if [ $? -ne 0 ]
then
  echo "Unable to complete setup"
  exit 1
fi

service rsyslog start 2>&1 | logger -t default -i -p local5.info

if [ $? -ne 0 ]
then
  echo "Error starting syslog"
  exit 1
fi

service ssh start 2>&1 | logger -t default -i -p local5.info

if [ $? -ne 0 ]
then
  echo "Error start SSH"
  exit 1
fi

service cron start 2>&1 | logger -t default -i -p local5.info

if [ $? -ne 0 ]
then
  echo "Error starting cron"
  exit 1
fi

sleep 3

env | grep GCS_BUCKET > /etc/environment

chown -R $SFTP_USER /var/landing/stage

python /opt/build/bin/format_logs.py

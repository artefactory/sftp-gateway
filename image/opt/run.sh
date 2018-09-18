#! /bin/bash

python /opt/build/bin/setup.py

if [ $? -ne 0 ]
then
  echo "Unable to complete setup"
  exit 1
fi

service rsyslog start

if [ $? -ne 0 ]
then
  echo "Error starting syslog"
  exit 1
fi

service ssh start

if [ $? -ne 0 ]
then
  echo "Error start SSH"
  exit 1
fi

nohup gcsfuse --key-file /var/secrets/credentials/key.json \
              --foreground \
              --debug_gcs \
              -o allow_other \
              --uid 9000 \
              --gid 9000 \
              $GCSSFTP_BUCKET \
              /var/landing/stage 2> /dev/null \
              | logger -t gcsfuse -i -p local5.info &

if [ $? -ne 0 ]
then
  echo "Error starting gcsfuse"
  exit 1
fi

sleep 3

chown $GCSSFTP_USER /var/landing/stage

python /opt/build/bin/format_logs.py

#! /bin/sh

upload_directory=$(mktemp -d)
payload_directory=${upload_directory}/payload/

mkdir -p ${payload_directory}

find /var/landing/stage/ingest -type f ! -iname "*.tmp" | xargs -I@ mv -v @ $payload_directory | logger -t syncer -i -p local5.info

if [ "$(ls -A $upload_directory)" ]; then
  /usr/bin/gsutil -m mv -n -L ${upload_directory}/transfer.log ${payload_directory}/* gs://${GCS_BUCKET} | logger -t syncer -i -p local5.info
  /usr/bin/python /opt/build/bin/read_report.py ${upload_directory}/transfer.log | logger -t syncer -i -p local5.info

  for errored_file in $(ls ${payload_directory}); do
    echo "Moving errored file ${payload_directory}/${errored_file} to /var/landing/stage/error" | logger -t syncer -i -p local5.info
    mv ${payload_directory}/${errored_file} /var/landing/stage/error
  done
else
  echo "No files to process" | logger -t syncer -i -p local5.info
fi

rm -rfv $upload_directory

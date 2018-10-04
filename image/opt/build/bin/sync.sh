#! /bin/sh

set -e

upload_directory=$(mktemp -d)

find /var/landing/stage/ingest -type f ! -iname "*.tmp" | xargs -I@ mv -v @ $upload_directory | logger -t syncer -i -p local5.info

if [ "$(ls -A $upload_directory)" ]; then
  /usr/bin/gsutil -q -m mv -n -L ${upload_directory}/transfer.log ${upload_directory}/* gs://${GCSSFTP_BUCKET}
  /usr/bin/python /opt/build/bin/read_report.py ${upload_directory}/transfer.log | logger -t syncer -i -p local5.info
  rm ${upload_directory}/transfer.log

  for errored_file in $(ls ${upload_directory}); do
    echo "Moving errored file ${upload_directory}/${errored_file} to /var/landing/stage/error" | logger -t syncer -i -p local5.info
    mv ${upload_directory}/${errored_file} /var/landing/stage/error
  done
else
  echo "No files to process" | logger -t syncer -i -p local5.info
fi

rm -rfv $upload_directory

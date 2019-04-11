import tempfile
import shutil
import os
import glob
import fnmatch
import command
import config
import csv
import re
import copy

import reraise
import log

if hasattr(config, 'APP_LANDING_EXCLUDE_PATTERNS'):
    _filters = config.APP_LANDING_EXCLUDE_PATTERNS.split(',')
else:
    _filters = []


def main():
    log.info("Starting sync")

    files = glob.glob(os.path.join(config.APP_LANDING_INGEST_DIR, '*'))

    for f in files:
        upload_file_to_buckets(f)
    else:
        log.info("No files to process")


def should_skip_file(f):
    for _filter in _filters:
        if fnmatch.fnmatch(f, _filter):
            return True
    return False


def upload_file_to_buckets(file_path):
    work_directory = tempfile.mkdtemp()

    log_labels = {'basename': os.path.basename(file_path), 'file': file_path}

    if should_skip_file(file_path):
        log.info("Skipping file {}".format(file_path), **log_labels)
        return

    working_copy = os.path.join(work_directory, os.path.basename(file_path))

    log.info("Copying {} to {}".format(file_path, working_copy), **log_labels)
    shutil.copy(file_path, working_copy)

    try:
        for bucket in config.APP_GCS_BUCKETS.split(','):
            upload_file_to_bucket(working_copy, bucket, log_labels)

        os.remove(file_path)
    except Exception as ex:
        error_destination = os.path.join(config.APP_LANDING_ERROR_DIR, os.path.basename(file_path))

        log.exception(ex)
        log.error("Moving {} to error directory {}".format(file_path, error_destination), **log_labels)
        shutil.move(file_path, error_destination)

    shutil.rmtree(work_directory)


def upload_file_to_bucket(file_path, bucket, log_labels):
    transfer_log_dir = tempfile.mkdtemp()
    transfer_log = os.path.join(transfer_log_dir, 'transfer.log')

    _local_labels = copy.copy(log_labels)
    _local_labels.update({
        'bucket': bucket
    })

    log.info("Uploading {} to {}".format(file_path, bucket), **_local_labels)

    upload_command = [
        '/usr/bin/gsutil',
        'cp',
        '-n',
        '-L',
        transfer_log,
        file_path,
        "gs://{}".format(bucket)
    ]

    try:
        try:
            command.run(upload_command, quiet=True)
        except Exception as ex:
            log.exception(ex)
            reraise.reraise()
        finally:
            parse_report(transfer_log, _local_labels)
    except Exception as ex:
        reraise.reraise()
    finally:
        shutil.rmtree(transfer_log_dir)


def parse_report(transfer_log, log_labels):
    errors = 0
    if os.path.isfile(transfer_log):
        with open(transfer_log, 'rb') as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                transfer_info = {convert(k): v for k, v in row.iteritems()}
                transfer_info.update(**log_labels)

                if transfer_info['result'] == 'OK':
                    log.info("Successfully uploaded file", event="successful_upload", **transfer_info)
                elif transfer_info['result'] == 'skip':
                    log.warn("Skipping existing file", event="skipping_upload", **transfer_info)
                else:
                    log.error("Error uploading file", event="failed_upload", **transfer_info)
                    errors += 1

    if errors > 0:
        raise Exception("Error uploading file")


def convert(name):
    name = name.replace(' ', '')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        log.exception(ex)

from parsers.extractor_set import ExtractorSet
from parsers.extractor import Extractor
import os

extractors = []

extractors.append(Extractor(
    'gcs_creating_directory',
    r'^.*<- CreateObject\(\"(?P<path>.+\/)\"\).*$',
    'info',
    'Creating GCS directory gs://%s/{path}' % os.environ['GCSSFTP_BUCKET']
))

extractors.append(Extractor(
    'gcs_created_directory',
    r'^.*-> CreateObject\(\"(?P<path>.+\/)\"\) \((?P<time>\d+(\.\d+)?)m?s\): OK.*$',
    'info',
    'Successfully created GCS directory gs://%s/{path}' % os.environ['GCSSFTP_BUCKET']
))

extractors.append(Extractor(
    'gcs_creating_file',
    r'^.*<- CreateObject\(\"(?P<path>.*[^/])\"\).*$',
    'info',
    'Creating GCS file gs://%s/{path}' % os.environ['GCSSFTP_BUCKET']
))

extractors.append(Extractor(
    'gcs_created_file',
    r'^.*-> CreateObject\(\"(?P<path>.*[^/])\"\) \((?P<time>\d+(\.\d+)?)m?s\): OK.*$',
    'info',
    'Successfully created GCS file gs://%s/{path}' % os.environ['GCSSFTP_BUCKET']
))

extractors.append(Extractor(
    'gcs_downloading_file',
    r'^.*<- Read\(\"(?P<path>.*[^/])\", \[.*$',
    'info',
    'Downloading GCS file gs://%s/{path}' % os.environ['GCSSFTP_BUCKET']
))

extractors.append(Extractor(
    'gcs_downloaded_file',
    r'^.*-> Read\(\"(?P<path>.*[^/])\", \[.+\)\) \((?P<time>\d+(\.\d+)?)m?s\): OK.*$',
    'info',
    'Successfully downloaded GCS file gs://%s/{path}' % os.environ['GCSSFTP_BUCKET']
))

extractor_set = ExtractorSet('gcsfuse', extractors)


def parse_gcsfuse(pid, message):
    global extractor_set
    return extractor_set.apply(pid, message)

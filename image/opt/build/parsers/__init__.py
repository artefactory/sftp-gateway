# flake8: noqa

from parsers.parse_gcsfuse import parse_gcsfuse
from parsers.parse_internal_sftp import parse_internal_sftp
from parsers.parse_sshd import parse_sshd

parsers = {
    'internal-sftp': parse_internal_sftp,
    'gcsfuse': parse_gcsfuse,
    'sshd': parse_sshd
}

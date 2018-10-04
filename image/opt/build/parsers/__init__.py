# flake8: noqa

from parsers.parse_internal_sftp import parse_internal_sftp
from parsers.parse_sshd import parse_sshd
from parsers.parse_syncer import parse_syncer
from parsers.parse_default import parse_default

parsers = {
    'internal-sftp': parse_internal_sftp,
    'syncer': parse_syncer,
    'sshd': parse_sshd,
    'default': parse_default
}

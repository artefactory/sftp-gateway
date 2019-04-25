from parsers.extractor_set import ExtractorSet
from parsers.extractor import Extractor

extractors = []

extractors.append(Extractor(
    'sftp_connected',
    r'^session opened for local user (?P<user>[^\s]+) from \[(?P<ip_address>\d+\.\d+\.\d+\.\d+)\]$',
    'info',
    'User {user} from {ip_address} connected to SFTP subsystem',
    ['user', 'ip_address']
))

extractors.append(Extractor(
    'sftp_disconnected',
    r'^session closed for local user (?P<user>[^\s]+) from \[(?P<ip_address>\d+\.\d+\.\d+\.\d+)\]$',
    'info',
    'User {user} from {ip_address} disconnected from SFTP subsystem',
    [],
    ['user', 'ip_address']
))

extractors.append(Extractor(
    'sftp_rename',
    r'^posix-rename old "(?P<old_path>.+?)" new "(?P<path>.+?)"$',
    'info',
    'Moved {old_path} to {path}',
    [],
    []
))

extractors.append(Extractor(
    'sftp_mkdir',
    r'^mkdir \"(?P<path>.+)\" flags.*$',
    'info',
    'Created directory {path}',
    [],
    ['path']
))

extractors.append(Extractor(
    'sftp_read_file',
    r'^close \"(?P<path>.+)\" bytes read (?P<bytes>\d+) written 0$',
    'info',
    'Downloaded file {path} ({bytes} bytes read)',
    [],
    ['path']
))

extractors.append(Extractor(
    'sftp_write_file',
    r'^close \"(?P<path>.+)\" bytes read 0 written (?P<bytes>\d+)$',
    'info',
    'Uploaded file {path} ({bytes} bytes written)',
    [],
    ['path']
))

extractors.append(Extractor(
    'sftp_error',
    r'sent status (?P<status>.+)$',
    'warn',
    '{status}',
    [],
    ['path']
))

extractor_set = ExtractorSet('internal-sftp', extractors)


def parse_internal_sftp(pid, message):
    return extractor_set.apply(pid, message)

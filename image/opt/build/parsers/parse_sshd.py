from parsers.extractor_set import ExtractorSet
from parsers.extractor import Extractor
from parsers.context import context_for

extractors = []

extractors.append(Extractor(
    'ssh_connection',
    r'^Connection from (?P<ip_address>\d+\.\d+\.\d+\.\d+).*$',
    'info',
    'Incoming SSH connection from {ip_address}'
))

extractors.append(Extractor(
    'ssh_authentication_successful',
    r'^Accepted publickey for (?P<user>[^\s]+) from (?P<ip_address>\d+\.\d+\.\d+\.\d+).*$',
    'info',
    'SSH Authentication successful for user {user} from {ip_address}',
    ['user', 'ip_address']
))

extractors.append(Extractor(
    'ssh_disconnection',
    r'^Disconnected from user (?P<user>[^\s]+) (?P<ip_address>\d+\.\d+\.\d+\.\d+).*$',
    'info',
    'User {user} from {ip_address} disconnected from SSH',
    [],
    ['user', 'ip_address']
))

extractors.append(Extractor(
    'ssh_authentication_failed',
    r'^Invalid user (?P<user>[^\s]+) from (?P<ip_address>\d+\.\d+\.\d+\.\d+).*$',
    'info',
    'SSH Authentication failed for user {user} from {ip_address}',
    [],
    ['user', 'ip_address']
))

extractors.append(Extractor(
    'ssh_authentication_failed',
    r'^Failed publickey for (?P<user>[^\s]+) from (?P<ip_address>\d+\.\d+\.\d+\.\d+).*$',
    'info',
    'SSH Authentication failed for user {user} from {ip_address}',
    [],
    ['user', 'ip_address']
))

extractors.append(Extractor(
    'ssh_authentication_failed',
    r'Connection closed by authenticating user (?P<user>[^\s]+) (?P<ip_address>\d+\.\d+\.\d+\.\d+) port (?P<port>\d+) \[preauth\]$',
    'warn',
    'SSH Authentication failed for user {user} from {ip_address}',
    [],
    ['user', 'ip_address']
))


def clone_context_to_child(pid, message, extracted_values):
    child_pid = int(extracted_values['child_pid'])
    context_for(child_pid).update(context_for(pid))
    return False


extractors.append(Extractor(
    'null',
    r'^User child is on pid (?P<child_pid>\d+).*$',
    'info',
    '#Unused',
    fn=clone_context_to_child
))

extractor_set = ExtractorSet('sshd', extractors)


def parse_sshd(pid, message):
    global extractor_set
    return extractor_set.apply(pid, message)

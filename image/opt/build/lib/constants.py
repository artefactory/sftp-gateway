import os


FORBIDDEN_USERNAMES = [u.split(':')[0] for u in open('/etc/passwd', 'rb').read().split()]
DEFAULT_UID = 9000
DEFAULT_GID = 9000
AUTHORIZED_KEYS_DIRECTORY = "/etc/ssh/authorized-keys/"

SECRETS_PATH = "/var/secrets/credentials/"
SECRET_GCPKEYFILE = os.path.join(SECRETS_PATH, "key.json")

TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'templates')
LANDING_DIRECTORY = "/var/landing"

SSHD_CONFIG_FILE = "/etc/ssh/sshd_config"
RSYSLOG_CONFIG_FILE = "/etc/rsyslog.conf"

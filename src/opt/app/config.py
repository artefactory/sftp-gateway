import os


for variable, value in os.environ.iteritems():
    locals()[variable.strip()] = value.strip()


FORBIDDEN_USERNAMES = [u.split(':')[0] for u in open('/etc/passwd', 'rb').read().split()]

APP_SFTP_AUTHORIZEDKEYS_KEYPATH = os.path.join(locals()['APP_SFTP_AUTHORIZEDKEYS_DIR'], locals()['APP_SFTP_USER'])

TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'templates')

SSH_DIR = "/etc/ssh"
SSHD_CONFIG_FILE = "/etc/ssh/sshd_config"
RSYSLOG_CONFIG_FILE = "/etc/rsyslog.conf"
RSYSLOG_DEFAULT_CONFIG_FILE = "/etc/rsyslog.d/50-default.conf"

ENVIRONMENT_FILE = "/etc/environment"
ENVIRONMENT_VARIABLE_PREFIXES = ['APP_', 'GCP_']


def get_template(template):
    template_with_extension = "{}.mustache".format(template)
    return os.path.join(TEMPLATE_DIRECTORY, template_with_extension)

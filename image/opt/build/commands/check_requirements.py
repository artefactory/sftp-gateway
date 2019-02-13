import lib.helpers as helpers
import lib.constants as const


def check_requirements():

    print "Checking requirements"

    if not helpers.has_value('SFTP_USER'):
        raise Exception("Missing SFTP_USER environment variable")

    if not helpers.has_value('GCS_BUCKET'):
        raise Exception("Missing GCS_BUCKET environment variable")

    username = helpers.get_user()

    if not (username and username not in const.FORBIDDEN_USERNAMES):
        raise Exception("SFTP_USER value is invalid")

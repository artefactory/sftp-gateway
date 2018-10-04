import lib.helpers as helpers
import lib.constants as const


def check_requirements():

    print "Checking requirements"

    if not helpers.has_value('GCSSFTP_USER'):
        raise Exception("Missing GCSSFTP_USER environment variable")

    if not helpers.has_value('GCSSFTP_SSH_PUBKEY'):
        raise Exception("Missing GCSSFTP_SSH_PUBKEY environment variable")

    if not helpers.has_value('GCSSFTP_BUCKET'):
        raise Exception("Missing GCSSFTP_BUCKET environment variable")

    username = helpers.get_user()

    if not (username and username not in const.FORBIDDEN_USERNAMES):
        raise Exception("GCSSFTP_USER value is invalid")

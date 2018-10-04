import os

import lib.constants as const
import lib.helpers as helpers


def create_service_account_key():

    print "Create service account"

    if helpers.has_value('GCSSFTP_SERVICE_ACCOUNT_KEY'):

        with open(const.SECRET_GCPKEYFILE, 'wb') as handle:
            handle.write(helpers.gcp_create_service_account_key())

        os.chmod(const.SECRET_GCPKEYFILE, 0644)
        os.chown(const.SECRET_GCPKEYFILE, const.DEFAULT_UID, const.DEFAULT_GID)

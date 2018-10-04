import lib.helpers as helpers
import lib.constants as const


def configure_gcloud():

    print "Configuring gcloud"

    auth = [
        "gcloud",
        "auth",
        "activate-service-account",
        "--key-file={}".format(const.SECRET_GCPKEYFILE)
    ]

    project = [
        "gcloud",
        "config",
        "set",
        "project",
        helpers.get_project_id()
    ]

    helpers.command(auth)
    helpers.command(project)



## Requirements

-   [Docker](https://docs.docker.com/install/)
-   [Python](https://www.python.org/downloads/)
-   Make ([Ubuntu](https://linuxize.com/post/how-to-install-gcc-compiler-on-ubuntu-18-04/), [Debian](https://linuxize.com/post/how-to-install-gcc-compiler-on-debian-10/), [Mac with Homebrew](https://formulae.brew.sh/formula/make), [Windows](https://stat545.com/make-windows.html))
-   If you want to deploy the cluster on Google Kubernetes Engine (GKE) or if you want to upload data on Google Cloud Storage (GCS) buckets, you will need to install the [Google Cloud SDK](https://cloud.google.com/sdk/install) (AKA `gcloud`)

For Kubernetes:

-   [Kubernetes](https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/)
-   [Helm](https://helm.sh/docs/intro/install/)


## Before you do anything

- Run `pip install -r requirements.txt -r dev-requirements.txt` before trying to build/configure anything.
- Run `export ENV=[NAME OF YOUR ENVIRONMENT]`
- Create an env file for your configuration with the following name `./env/${ENV}` (see next step [Environment Configuration](./1-EnvironmentConfiguration.md))

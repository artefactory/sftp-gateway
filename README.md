# nautilus-gcs-sftp-gateway

This is a Docker image containing an SSH server and a gsutil rsync script, allowing to create a SFTP-to-GCS gateway server. Once deployed, you can connect to the SFTP server and read/write files that are immediately synchronised to GCS.

The repository contains the appropriate files to deploy the container to Kubernetes.

## Maintainer
- Douglas Willcocks (@d-tw or douglas@artefact.com)

## Before you do anything

- Run `pip install -r requirements.txt` before trying to build/configure anything.
- Create an env file for your configuration in `./env` (see Configuration below)

## Requirements

-   Docker
-   Python
-   Make
-   Google Cloud SDK (AKA `gcloud`)
-   jq

For Kubernetes:

-   Kubernetes
-   Helm

## Overview

When you run a container based on this image, it creates an SFTP server that can only be accessed by one specified user, and moves uploaded data to one or more specified GCS buckets.

The user and the buckets are provided at runtime via container Environment variables. When the container starts, it uses the Environment variables to generate the appropriate configuration files and start the services. The container does not persist any data.

The container does not contain any credentials, they must be provided at deployment time via a mounted secrets volume on Kubernetes, or a mounted volume for vanilla Docker. See below for more information.

## Usage

### Configuration
All of the configuration is managed through the environment files stored in the `./env` directory. There is a `common` environment file that contains the majority of the configuration directives, and typically doesn't need to be changed. You can then create additional configuration files for different environments/clients, such as `dev`, `prod`, or `***REMOVED***`.

The environment variables specified in the environment files override the values defined in the `common` file during processing.

These environment files are used to automatically generate various other configuration files (Helm `values.yaml` files, Kubernetes `configmap` files, etc.) – you shouldn't need to change anything other than the environment config files to configure any aspect of the system.

You can read the `common` and `sample` files in `./env` to understand what the configuration directives are for.

### Credentials
In order for the service to run, you need to generate/provide various credential files:

- GCP Service Account key file, to grant the image the right to upload files to a GCS bucket
- SSH Public key file, the public par of the public-private key used to connect to the SFTP server
- SSH Host keys, the server's identity keys

#### Vanilla Docker
If you're using vanilla Docker, a directory containing the above secret files should be mounted onto the container to the path configured by `$APP_SECRETS_DIR` (by default, `/var/run/secrets/nautilus-gcs-sftp-gateway-${ENV}`).

#### Kubernetes
If you're using Kubernetes, the credentials should be provided through mounted secrets volume. It's recommended to use the provided Helm Chart to handle all of the specfile generation and deployment. See the Helm section below for more info.

#### GCP Service Account
Your container will need a GCP Service Account in order to write to GCS buckets; the service account key file should be provided as a secret to the container with the name defined by `$GCP_SERVICEACCOUNT_KEY_NAME` (by default, `nautilus-gcs-sftp-gateway-${ENV}-sa-key.key`)

You can generate your own manually through the [GCP UI](https://cloud.google.com/iam/docs/creating-managing-service-account-keys), or by running the following command:

```shell
ENV=your-env-name make create_gcp_service_account_key
```

The service account key will be placed in `./credentials/<your-env-name>/files/`.

#### SSH Public Key
The SFTP server only accepts public/private key authentication, you need to create or provide a public/private key pair and mount the public key in the container as a secret.

You can generate your own public/private key pair by running the command:

```shell
ENV=your-env-name make create_ssh_key
```

The keys will be placed in `./credentials/<your-env-name>/files/`.

#### SSH Host Keys (Optional)
When you connect to an SFTP server, before verifying your identity it sends you a unique signature that identifies the server. This signature is typically stored by SFTP clients to verify the identity of the server the next time you connect.

As the docker containers are emphemeral, different instances of the image will have different host keys, which can cause SFTP clients to complain with the following error:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is x.
Please contact your system administrator.
```

To avoid this, you can provide your own SSH host keys that will be used for each container. The host keys should be mounted to `$APP_SECRETS_DIR`, and have the `ssh_host_` prefix:

```shell
% ls -l
-rw-------  1 d_tw  staff  1381 Apr  9 19:23 ssh_host_dsa_key
-rw-------  1 d_tw  staff   513 Apr  9 19:23 ssh_host_ecdsa_key
-rw-------  1 d_tw  staff   411 Apr  9 19:23 ssh_host_ed25519_key
-rw-------  1 d_tw  staff  3381 Apr  9 19:23 ssh_host_rsa_key
```

You can generate your own SSH host keys by running:

```shell
ENV=your-env-name make create_ssh_host_keys
```

The files will be placed in `./credentials/<your-env-name>/files/`.

### Building the Docker image

To build the image, just run:

```shell
ENV=your-env-name make docker_build
```

You can also publish the image to a registry:

```shell
ENV=your-env-name make docker_publish
```

### Running as standalone Docker
To run the image standalone, you need to provide 3 things:

- Environment variables via the `--env-file` option
- A secrets volume mount
- A port binding

Having written your config file in `./env`, run

```shell
ENV=your-env-name make generate_config
```

This will output a resolved config file to `./config/<your-env-name>`.

You can run the docker image with:

```shell
docker run --rm -it --env-file ./config/${ENV} \
                    -v ./credentials/${ENV}/files:$APP_SECRETS_DIR \
                    -p ${HOST_PORT}:${APP_SFTP_PORT} \
                    ${APP_DOCKER_IMAGE}
```

Where `HOST_PORT` is the port on the host machine to which docker should bind (probably not 22, since you might already have an SSH service), `ENV` is the name of your environment, and the `APP_*` variables are the values taken from `./config/<your-env-name>`.

### Deploying to GKE
The project contains a Helm Chart that can deploy the service to a Kubernetes cluster.

You can setup Helm on your cluster, if not already done, by running:

```shell
make helm_setup
```

Once that's done, you can just run:

```
ENV=your-env-name make helm_install
```

This will automatically pick up any changes made to the relevant files in `./env` and `./credentials`, regenerate config, generate the approriate `values.yaml` file for Helm, and deploy the changes to your Kubernetes cluster.


#### Generating a fixed IP address

In order to expose the SFTP server, you need to reserve a static IP address that will be used by Kubernetes. The IP address needs to be in the same zone as the Kubernetes cluster.

```
gcloud compute addresses create [ADDRESS_NAME] --region [KUBE_ZONE] --ip-version IPV4
```

### Connecting to the SFTP server

For various technical reasons relating to [SFTP Chrooting](https://wiki.archlinux.org/index.php/SFTP_chroot), the SFTP users will see two directories (`stage` and `dev`) when they connect to the server.

Only the contents of the `stage/ingest` directory are mapped to GCS.


### Logging output
The docker container logs various events to STDOUT, each log entry is a JSON object that is compatible with [Stackdriver Structured Logs](https://cloud.google.com/logging/docs/structured-logging).

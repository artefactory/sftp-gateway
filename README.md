# gcs-sftp-gateway

This is a Docker image containing an SSH server and [gcsfuse](https://cloud.google.com/storage/docs/gcs-fuse), allowing to create a SFTP-to-GCS gateway server. Once deployed, you can connect to the SFTP server and read/write files that are immediately synchronised to GCS.

The repository also contains the appropriate files to deploy the container to Kubernetes.

## Requirements

- Docker
- Python
- Make
- Google Cloud SDK (AKA `gcloud`)
- Kubernetes (Optional)

## Overview

When you run a container based on this image, it creates an SFTP server that can only be accessed by one specified user, and only connect to one specified GCS bucket.

The user and the bucket are provided at runtime via container Environment variables. When the container starts, it uses the Environment variables to generate the appropriate configuration files and start the services. The container does not persist any data.

The container does not contain any credentials, they must be provided at deployment time via a mounted volume. See below for more information.

## Usage

#### Setup

Install the required dependencies:

```
pip install -r requirements.txt
```

#### Makefile
Most of the commands to use the container are in a `Makefile`, which simplifies all of the steps. You don't need to use the `Makefile` if you want to go off the beaten path.

The header of the `Makefile` contains a number of variables that you can change, such as the docker image name, the container registry to be used, etc.

#### Environment Variables
The different `Makefile` commands rely on Environment variables to run correctly. The `Makefile` will not run unless you have defined the following variables:

| Variable | Description | Example |
| --- | --- | ---: |
| `PROJECT_ID `| The ID of the GCP Project | `monoprix-datalake-dev` |
| `GCSSFTP_USER` | The username that will be used to access the SFTP server | `monoprix` |
| `GCSSFTP_BUCKET` | The name of the GCS bucket that will be used (must be in the same GCP Project) | `monoprix-datalake-ingest-dev` |

To set Environment variables, use the `export` command:

```
export PROJECT_ID=monoprix-datalake-dev
```

#### Credentials

For the container to run correctly, it requires you to provide credentials. The different systems on the container look for the files in the following locations on the docker image:

| Credential | Description |Path |
| --- | --- | ---: |
| SSH Public Key| Allows the external user with the corresponding Private Key to connect to the SFTP server | `/var/secrets/credentials/sftp.key.pub` |
| Google Service Account JSON key | Allows `gcsfuse` to connect to the GCS bucket | `/var/secrets/credentials/key.json` |

These values **must** be provided for the container to run. The values can be provided by mounting a volume on the container.

##### Generating Credentials

You can use the `Makefile` to generate credentials if you don't already have them.

```
make credentials
```

This command will:

- Create a `./credentials/{PROJECT_ID}/` folder
- Generate a new Public/Private key pair in the folder
- Create a GCP Service account
- Create a new Service account JSON key in the folder

#### Directories

For various technical reasons relating to [SFTP Chrooting](https://wiki.archlinux.org/index.php/SFTP_chroot), the SFTP users will see two directories (`stage` and `dev`) when they connect to the server.

Only the contents of the `stage` directory are mapped to GCS.

### Building the image
To build the image, just run:

```
make docker_build
```

You can also publish the image to a registry:

```
make docker_publish
```

### Running the image on Docker

You can run the container with Docker with the following command (note: this doesn't detach):

```
docker run -a STDOUT -it \
           --mount type=bind,source=$$(pwd)/credentials/,target=/var/secrets/credentials/ \
           --cap-add SYS_ADMIN --device /dev/fuse \
           --env GCSSFTP_USER=${GCSSFTP_USER} \
           --env GCSSFTP_BUCKET=${GCSSFTP_BUCKET} \
           -P \
           {DOCKER_IMAGE}

```

Alternatively

```
make docker_run
```
### Running the image on Kubernetes

Assuming you have a Kubernetes cluster, you can run the image as a Pod, exposed via an internal LoadBalancer Service. This repository contains the spec files required to generate a Service and a High-Availability Deployment of 2 containers.

More information on the Kubernetes config can be found in the spec files in the `./kube` directory.

If you're feeling brave, you can (after changing the variables in the `Makefile`) just run

```
make kubernetes_run
```

Which will:

- Build the image
- Publish the image to the registry
- Create a ClusterRoleBinding on K8S giving you admin rights
- Create a GCP Service account to be used by the container
- Create a GCP Service account key
- Generate an SSH key
- Create a K8S Secret, containing the credentials
- Create a K8S Service with a NodePort
- Create a K8S Deployment with 2 running instances

### Logging

The relevant logs from the three primary systems on the container are sent to STDOUT in a standard format for ease of monitoring.

The log entries are in a JSON format which is compatible with Stackdriver, so if you run your container on GCS or Kubernetes you get logging for free :)

```json
{
    "message": "User monoprix from 10.222.0.18 connected to SFTP subsystem",
    "timestamp": "2018-09-18T09:13:37Z",
    "severity": "INFO",
    "labels": {
      "event": "sftp_connected",    
      "ip_address": "10.222.0.18",
      "pid": 59,
      "process": "internal-sftp",    
      "user": "monoprix"    
    }
}
```

# gcs-sftp-gateway

This is a Docker image containing an SSH server and a gsutil rsync script, allowing to create a SFTP-to-GCS gateway server. Once deployed, you can connect to the SFTP server and read/write files that are immediately synchronised to GCS.

The repository contains the appropriate files to deploy the container to Kubernetes.

## Requirements

-   Docker
-   Python
-   Make
-   Google Cloud SDK (AKA `gcloud`)
-   Kubernetes

## Overview

When you run a container based on this image, it creates an SFTP server that can only be accessed by one specified user, and only connect to one specified GCS bucket.

The user and the bucket are provided at runtime via container Environment variables. When the container starts, it uses the Environment variables to generate the appropriate configuration files and start the services. The container does not persist any data.

The container does not contain any credentials, they must be provided at deployment time via a mounted secrets volume. See below for more information.

## Usage

#### Setup

Install the required dependencies:

```
pip install -r requirements.txt
```

#### Makefile

Most of the commands to use the container are in a `Makefile`, which simplifies all of the steps. You don't need to use the `Makefile` if you want to go off the beaten path.

The header of the `Makefile` contains a number of variables that you can change, such as the docker image name, the container registry to be used, etc.

##### Config Environments

The different `Makefile` commands rely on Environment variables to run correctly. You need to create an environment file in the `env` directory, with the following variables:

| Variable          |  Description                                                                   |                        Example |
| ----------------- | ------------------------------------------------------------------------------ | -----------------------------: |
| GCS_BUCKET        | The name of the GCS bucket that will be used (must be in the same GCP Project) | `***REMOVED***-datalake-manual-dev` |
| PROJECT_ID        | The ID of the GCP Project                                                      |                  `datalakempx` |
| SFTP_USER         | The username that will be used to access the SFTP server                       |                     `***REMOVED***` |
| SFTP_IP           | The fixed IP address that will expose the SFTP server (see below)              |               `35.228.205.241` |
| KUBE_CLUSTER_NAME | The Kubernetes cluster name                                                    |                    `ingestion` |
| KUBE_ZONE         | The Kubernetes cluster zone                                                    |              `europe-north1-a` |

You can then run the Makefile with the name of the environment (for example, for an env file name `env/production`):

```
ENV=production make kubernetes_run
```

##### Generating a fixed IP address

In order to expose the SFTP server, you need to reserve a static IP address that will be used by Kubernetes. The IP address needs to be in the same zone as the Kubernetes cluster.

```
gcloud compute addresses create [ADDRESS_NAME] --region [KUBE_ZONE] --ip-version IPV4
```

#### Credentials

For the container to run correctly, it requires you to provide a GCP service account key and an SFTP public key.
You can use the `Makefile` to generate credentials if you don't already have them.

```
ENV=dev make credentials
```

This command will:

-   Create a `./credentials/{ENV}/` folder
-   Generate a new Public/Private key pair in the folder
-   Create a GCP Service account
-   Create a new Service account JSON key in the folder

**Note:** You need to grant the appropriate GCS access rights to the service account.

If you want to provide your own service account key or public SFTP key, you can just put them in the `./credentials/{ENV}` folder called `key.json` and `sftp.key.pub` respectively.

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

### Running the image on Kubernetes

Assuming you have a Kubernetes cluster, you can run the image as a Pod, exposed via a LoadBalancer Service. This repository contains the spec files required to generate a Service and a High-Availability Deployment of 2 containers.

More information on the Kubernetes config can be found in the spec files in the `./kube` directory.

If you're feeling brave, you can just run

```
make kubernetes_run
```

Which will:

-   Build the image
-   Publish the image to the registry
-   Create a ClusterRoleBinding on K8S giving you admin rights
-   Create a GCP Service account to be used by the container
-   Create a GCP Service account key
-   Generate an SSH key
-   Create a K8S Secret, containing the credentials
-   Create a K8S Service with a NodePort
-   Create a K8S Deployment with 2 running instances

### Logging

The relevant logs from the three primary systems on the container are sent to STDOUT in a standard format for ease of monitoring.

The log entries are in a JSON format which is compatible with Stackdriver, so if you run your container on GCS or Kubernetes you get logging for free :)

```json
{
    "message": "User ***REMOVED*** from 10.222.0.18 connected to SFTP subsystem",
    "timestamp": "2018-09-18T09:13:37Z",
    "severity": "INFO",
    "labels": {
      "event": "sftp_connected",    
      "ip_address": "10.222.0.18",
      "pid": 59,
      "process": "internal-sftp",    
      "user": "***REMOVED***"    
    }
}
```

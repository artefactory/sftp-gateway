
# nautilus-sftp-gateway

![](https://nautilus-badger.appspot.com/get_badge/4d29c65d5f4d21f543ea2389e29fc7bcb621e7ef649ce070e6a47c1b5fbb86e9)
![](https://nautilus-badger.appspot.com/get_badge/31b1704918e14bb03933a6068e18a8afc09d725ceefc0e78a06267c65ccd07c2)
![](https://nautilus-badger.appspot.com/get_badge/0bc8e88d64bc4046cb18d70e0321de06405a51c8c889e7d8b903599b740a205f)
![](https://nautilus-badger.appspot.com/get_badge/52471cb3ec0b885cd51803a988f2c01df7a6d054f1398efd1d052f3967667230)


## Architecture

![Nautilus SFTP Gateway architecture](./Nautilus_SFTP_Gateway_architecture.png)


This is a Docker image containing a SSH server and an INotify daemon allowing to create a SFTP gateway server. Once deployed, you can connect to the SFTP server and read/write files that are immediately synchronised to GCS or other cloud storage services.

The repository contains the appropriate files to deploy the container to Kubernetes.


## Maintainer

- Cédric Magnan (@Cedric-Magnan or cedric.magnan@artefact.com)


## Overview

When you run a container based on this image, it creates a SFTP server that can only be accessed by specified users, and moves uploaded data to one or more specified buckets.

The users and the buckets are provided at runtime via container Environment variables. When the container starts, it uses the Environment variables to generate the appropriate configuration files and start the services. The container does not persist any data.

The container does not contain any credentials, they must be provided at deployment time via a mounted secrets volume on Kubernetes, or a mounted volume for vanilla Docker. See below for more information.


## Quick setup

- 1/ Setup your environment by running `export ENV=dev` (here `dev` for example). Also run the following command : `export PYTHONPATH=$PYTHONPATH:.`
- 2/ Fill in your configuration by copying the `./config/example.yaml` into a new `./config/${ENV}.yaml` file and replace the values by the ones you need.
- 3/ Add your secrets into the `./credentials/${ENV}` folder or let the project generate them for you.
- 4/ Test your configuration by running the following command : `make docker_run`
- 5/ Install Tiller on your Kubernetes cluster by running `make helm_setup`, if not already done.
- 6/ Generate or copy an existing an IPv4 address that can be used by your Kubernetes cluster in your configuration file under APP -> SERVICE_IP.
- 7/ Deploy the SFTP on Kubernetes my running the following command : `make helm_install`


## Table of contents

- [0 - Installation](./0-Installation.md)
- [1 - Environment configuration](./1-EnvironmentConfiguration.md)
- [2 - Keys generation](./2-KeysGeneration.md)
- [3 - Cloud configuration](./3-CloudConfiguration.md)
- [4 - Docker configuration](./4-DockerConfiguration.md)
- [5 - Cluster configuration](./5-ClusterConfiguration.md)
- [6 - SFTP connection](./6-SFTPConnection.md)



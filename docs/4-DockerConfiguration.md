
This step requires steps :
- [2 - Keys generation](./docs/2-KeysGeneration.md)
- [3 - Cloud configuration](./docs/3-CloudConfiguration.md)


If you're using vanilla Docker, a directory containing the above secret files should be mounted onto the container to the path configured by `${APP_SECRETS_DIR}` (by default, `/var/run/secrets/nautilus-sftp-${ENV}`).


### Building the Docker image

To build the image, just run:

```shell
make docker_build
```

You can also publish the image to a registry:

```shell
make docker_publish
```


### Running as standalone Docker

You can run the docker image with:
```shell
make docker_run
```

To connect to the docker container, you can use docker exec into the container using the following command :
```shell
docker exec -it $(docker ps | grep ${APP_DOCKER_IMAGE} | tr -s " " | cut -d " " -f 1) /bin/sh
```
or you can use the SFTP command to connect to the local SFTP server :
```shell
sftp -P ${APP_HOST_PORT} -i $(pwd)/credentials/${ENV}/users/${APP_SFTP_USER}/rsa-key ${APP_SFTP_USER}@0.0.0.0:ingest/
```


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

You can load these configurations using the following command :
```shell
source ./config/${ENV}
```

You can run the docker image with:

```shell
docker run --rm -it --env-file ./config/${ENV} \
                    -v $(pwd)/credentials/${ENV}/files:${APP_SECRETS_DIR} \
                    -p ${APP_HOST_PORT}:${APP_SFTP_PORT} \
                    ${APP_DOCKER_IMAGE}
```

Where `APP_HOST_PORT` is the port on the host machine to which docker should bind (probably not 22, since you might already have an SSH service), `ENV` is the name of your environment, and the `APP_*` variables are the values taken from `./config/<your-env-name>`.


To connect to the docker container, you can use docker exec into the container using the following command :
```shell
docker exec -it $(docker ps | grep ${APP_DOCKER_IMAGE} | tr -s " " | cut -d " " -f 1) /bin/sh
```
or you can use the SFTP command to connect to the local SFTP server :
```shell
sftp -P ${APP_HOST_PORT} -i $(pwd)/credentials/${ENV}/files/${APP_SFTP_PRIVATEKEY_NAME} ${APP_SFTP_USER}@0.0.0.0:stage/ingest/
```

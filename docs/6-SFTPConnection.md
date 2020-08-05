
[Home](./#-Home.md)

This step requires one of the following steps :
- [4 - Docker configuration](./4-DockerConfiguration.md)
- [5 - Cluster configuration](./5-ClusterConfiguration.md)


For various technical reasons relating to [SFTP Chrooting](https://wiki.archlinux.org/index.php/SFTP_chroot), the SFTP users won't be able to send data to the Cloud Storage services from their root folders.

Only the contents of the `ingest` directory are mapped to Cloud Storage services.

To connect to the SFTP, you can use the following command :
```shell
sftp -P ${APP_HOST_PORT} -i $(pwd)/credentials/${ENV}/users/${APP_SFTP_USER}/rsa-key ${APP_SFTP_USER}@{APP_SERVICE_IP}:ingest/
```


[Home](./#-Home.md)

This step requires steps :
- [1 - Environment configuration](./1-EnvironmentConfiguration.md)


#### SSH Public Key

The SFTP server only accepts public/private key authentication, you need to create or provide a public/private key pair and mount the public key in the container as a secret.

You can generate the password and public/private key pair for all users added in the `USERS` configuration variable of the YAML file by running the command:

```shell
make create_ssh_keys
```

The keys will be placed in the `./credentials/${ENV}/users/${APP_USERNAME}/` folder. The generated files will be `rsa-key`, `rsa-key.pub` and `password`. Be sure to follow this convention if you want to provide you own keys and passwords.


#### SSH Host Keys (Optional)

When you connect to an SFTP server, before verifying your identity it sends you a unique signature that identifies the server. This signature is typically stored by SFTP clients to verify the identity of the server the next time you connect.

As the docker containers are ephemeral, different instances of the image will have different host keys, which can cause SFTP clients to complain with the following error:

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

To avoid this, you can provide your own SSH host keys that will be used for each container. The host keys should be mounted to `$APP_SECRETS_DIR/internal/`, and have the `ssh-host-` prefix:

```shell
% ls -l
-rw-------  1 d_tw  staff  1381 Apr  9 19:23 ssh-host-dsa-key
-rw-------  1 d_tw  staff   513 Apr  9 19:23 ssh-host-ecdsa-key
-rw-------  1 d_tw  staff   411 Apr  9 19:23 ssh-host-ed25519-key
-rw-------  1 d_tw  staff  3381 Apr  9 19:23 ssh-host-rsa-key
```

You can generate your own SSH host keys by running:

```shell
make create_ssh_host_keys
```

The files will be placed in the `./credentials/${ENV}/internal/` folder.




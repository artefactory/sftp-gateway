
#### SSH Public Key
The SFTP server only accepts public/private key authentication, you need to create or provide a public/private key pair and mount the public key in the container as a secret.

You can generate your own public/private key pair by running the command:

```shell
ENV=your-env-name make create_ssh_key
```

The keys will be placed in `./credentials/<your-env-name>/`.

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

The files will be placed in `./credentials/<your-env-name>/`.


This step requires steps :
- [0 - Installation](./0-Installation.md)


All of the configuration is managed through the environment files stored in the `./env` directory. There is a `common` environment file that contains the majority of the configuration directives, and typically doesn't need to be changed. You can then create additional configuration files for different environments/clients, such as `dev` or `prod` for example.
The environment variables specified in the environment files override the values defined in the `common` file during processing.


These environment files are used to automatically generate various other configuration files (Helm `values.yaml` files, Kubernetes `configmap` files, etc.) – you shouldn't need to change anything other than the environment config files to configure any aspect of the system.
You can read the `common` and `sample` files in `./env` folder to understand what the configuration directives are for.


Furthermore, you can manage each user by creating configuration directives in the `./env/users/` folder.
You can read the and `sample` file in `./env/users` folder to understand what the user configuration directives are for.
Each bucket configured in the user configuration directive will be updated whenever a file is uploaded to the `ingest` folder


Once you filled in all the configuration directives, you can run the following command :

```shell
make generate_config
```

This will output a resolved config file to `./config/${ENV}`.

You can load these configurations in your terminal using the following command :
```shell
source ./config/${ENV}
```

[Home](./*-Home.md)

This step requires steps :
- [0 - Installation](./0-Installation.md)


All of the configuration is managed through a single environment file stored in the `./config` directory.

These environment files are used to automatically generate various other configuration files (Helm `values.yaml` files, Kubernetes `configmap` files, etc.) – you shouldn't need to change anything other than the environment config files to configure any aspect of the system.
You can read the `example.yaml` file in `./config` folder to understand what the configuration directives are for.

Furthermore, you can create specific users by adding them in the `USERS` variable of the configuration YAML file.
Each bucket configured in the user configuration directive will be updated whenever a file is uploaded to the `ingest` folder.

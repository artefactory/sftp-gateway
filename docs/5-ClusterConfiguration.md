
[Home](./#-Home.md)

This step requires steps :
- [2 - Keys generation](./2-KeysGeneration.md)
- [3 - Cloud configuration](./3-CloudConfiguration.md)


#### Generating a fixed IP address

In order to expose the SFTP server, you need to reserve a static IP address that will be used by Kubernetes. The IP address needs to be in the same zone as the Kubernetes cluster.

For Google Cloud :
```shell
gcloud compute addresses create ${APP_NAME}-ip --region ${K8S_REGION} --ip-version IPV4
```

Once this is done, you can update the APP_SERVICE_IP environment variable in the `./env/${ENV}` file.


### Deploying to the Kubernetes cluster

If you're using Kubernetes, the credentials should be provided through mounted secrets volume.

This project contains a Helm Chart that can deploy the service to a Kubernetes cluster.

First connect kubectl to the Kubernetes cluster by using the following command :
```shell
make setup_kubernetes_access
```

You can setup Helm on your cluster, if not already done, by running:
```shell
make helm_setup
```

Once that's done, you can just run:
```shell
make helm_install
```

This will automatically pick up any changes made to the relevant files in `./config/${ENV}` and `./credentials/${ENV}`, regenerate config, generate the approriate `values.yaml` file for Helm, and deploy the changes to your Kubernetes cluster.
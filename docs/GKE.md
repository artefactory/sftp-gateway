
#### Generating a fixed IP address

In order to expose the SFTP server, you need to reserve a static IP address that will be used by Kubernetes. The IP address needs to be in the same zone as the Kubernetes cluster.

```
gcloud compute addresses create ${APP_NAME}-ip --region ${K8S_REGION} --ip-version IPV4
```


### Deploying to GKE
The project contains a Helm Chart that can deploy the service to a Kubernetes cluster.

First connect kubectl to the Kubernetes cluster by using the following command :
```shell
ENV=your-env-name make setup_kubernetes_access
```


You can setup Helm on your cluster, if not already done, by running:

```shell
ENV=your-env-name make helm_setup
```

Once that's done, you can just run:

```shell
ENV=your-env-name make helm_install
```

This will automatically pick up any changes made to the relevant files in `./env` and `./credentials`, regenerate config, generate the approriate `values.yaml` file for Helm, and deploy the changes to your Kubernetes cluster.
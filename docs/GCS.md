

#### GCP Service Account
Your container will need a GCP Service Account in order to write to GCS buckets; the service account key file should be provided as a secret to the container with the name defined by `$GCP_SERVICEACCOUNT_KEY_NAME` (by default, `nautilus-sftp-gateway-${ENV}-sa-key.key`)

You can generate your own manually through the [GCP UI](https://cloud.google.com/iam/docs/creating-managing-service-account-keys), or by running the following command:

```shell
ENV=your-env-name make create_gcp_service_account_key
```

The service account key will be placed in `./credentials/<your-env-name>/files/`.

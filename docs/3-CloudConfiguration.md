
This step requires steps :
- [1 - Environment configuration](./docs/1-EnvironmentConfiguration.md)


#### GCP Service Account
Your container will need a GCP Service Account in order to write to GCS buckets; the service account key file should be provided as a secret to the container with the name defined by `$GCP_SERVICEACCOUNT_KEY_NAME` in the `./env/config/gcs` file
For each user of the `./env/users/` folder, if the user has configured the variables `APP_GCS_BUCKETS` and `GCP_BUCKET_PROJECT_IDS`, you'll need to add service account keys for the user for each distinct GCP_BUCKET_PROJECT_ID.

You can generate your own manually through the [GCP UI](https://cloud.google.com/iam/docs/creating-managing-service-account-keys), or by running the following command:

```shell
make create_gcp_service_account_keys
```

This will create Google Service Accounts with the role `roles/storage.objectAdmin` and Goocle CLoud Service Accounts Keys for each project and each user if the user has buckets configured for this project.

The service account keys follow this naming convention :
`./credentials/${ENV}/users/${APP_USERNAME}/google/${GCP_BUCKET_PROJECT_ID}.json`

You can use you own keys for each user but if so, be sure to follow the naming convention and that the service account has valid roles.



[Home](./#-Home.md)

This step requires steps :
- [1 - Environment configuration](./1-EnvironmentConfiguration.md)


#### GCP Service Account
Your container will need a GCP Service Account in order to write to GCS buckets; the service account key file should be provided as a secret to the container.
For each user of the `USERS` configuration variable of the YAML file, if the user has configured the `GCP_PROJECTS` and the `BUCKETS` variables, you'll need to add service account keys for the user for each distinct GCP project ID.

You can generate your own manually through the [GCP UI](https://cloud.google.com/iam/docs/creating-managing-service-account-keys), or by running the following command:

```shell
make create_gcp_service_account_keys
```

This will create Google Service Accounts with the role `roles/storage.objectAdmin` and Google Cloud Service Accounts Keys for each project and each user if the user has buckets configured for this project.

The service account keys follow this naming convention :
`./credentials/${ENV}/users/${APP_USERNAME}/google/${GCP_BUCKET_PROJECT_ID}.json`


#### AWS Access Keys
Your container will need an AWS Access Key in order to write to S3 buckets; the access key file should be provided as a secret to the container.
For each user of the `USERS` configuration variable of the YAML file, if the user has configured the `AWS_ACCOUNTS` and the `BUCKETS` variables, you'll need to add access keys for the user for each distinct AWS account ID.

You can generate your own manually through the [AWS UI](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html), or by running the following command:

```shell
make create_aws_access_keys
```

This will create AWS users with the Permission Boundary `s3:*` allowed for all resources and user access keys for each account and each user if the user has buckets configured for this account.

The service account keys follow this naming convention :
`./credentials/${ENV}/users/${APP_USERNAME}/aws/${S3_BUCKET_ACCOUNT_ID}.json`


You can use you own keys for each user but if so, be sure to follow the naming convention and that the service account has valid roles.




source config/${ENV}

config_exists=$(cat ~/.docker/config.json | grep $APP_DOCKER_REGISTRY)
if [[ "${config_exists}" != "" ]]
	echo "A configuration already exists but you may still need to re-authenticate to your registry"
else
	echo "
Please setup your docker configuration by using one of the following tools

	Google Cloud Platform :
	https://cloud.google.com/sdk/gcloud/reference/auth/configure-docker
	gcloud auth configure-docker REGISTRY_NAME

	Azure :
	https://docs.microsoft.com/en-US/azure/container-registry/container-registry-get-started-docker-cli
	az acr login --name REGISTRY_NAME

	AWS :
	https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth
	aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com

	### TODO : Test this docker registry authentication method ###
	Alicloud :
	https://www.alibabacloud.com/help/doc-detail/60743.htm
	docker login registry.cn-REGION.aliyuncs.com
	"
fi
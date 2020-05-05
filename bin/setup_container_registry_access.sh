# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#!/bin/sh

APP_DOCKER_REGISTRY=$(cat config/${ENV}.yaml | awk '/DOCKER_REGISTRY:/ {print $2}')
config_exists=$(cat ~/.docker/config.json | grep $APP_DOCKER_REGISTRY)
if [[ "${config_exists}" != "" ]]
then
	echo "A container registry configuration already exists but you may still need to re-authenticate to your registry"
else
	echo "
Please setup your docker configuration by using one of the following tools

	Google Cloud Platform :@
	https://cloud.google.com/sdk/gcloud/reference/auth/configure-docker
	gcloud auth configure-docker REGISTRY_NAME

	Azure :
	https://docs.microsoft.com/en-US/azure/container-registry/container-registry-get-started-docker-cli
	az acr login --name REGISTRY_NAME

	AWS :
	https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth
	aws ecr get-login-password --region REGION | docker login --username AWD --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com

	### TODO : Test this docker registry authentication method ###
	Alicloud :
	https://www.alibabacloud.com/help/doc-detail/60743.htm
	docker login registry.cn-REGION.aliyuncs.com
	"
fi
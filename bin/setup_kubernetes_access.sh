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

K8S_CLUSTER_NAME=$(cat config/${ENV}.yaml | awk '/CLUSTER_NAME:/ {print $2}')
context_exists=$(kubectl config use-context ${K8S_CLUSTER_NAME})
if [[ "${context_exists}" != "" ]]
then
	kubectl get all -A & sleep 5 ; kill $!;
	if [[ $? == 0 ]]
	then
	    echo "Authentication to the ${K8S_CLUSTER_NAME} cluster is not working properly. Please update your kubeconfig file..."
	else
		echo "Authentication to the ${K8S_CLUSTER_NAME} cluster is working."
	fi
else
	echo "
Please setup your cluster configuration by using one of the following tools

	Google Cloud Platform :
	https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl
	gcloud --project ${GCP_PROJECT_ID} container clusters get-credentials K8S_CLUSTER_NAME --zone K8S_ZONE

	Azure :
	https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest#az-aks-get-credentials
	az aks get-credentials --name K8S_CLUSTER_NAME --resource-group RESSOURCE_GROUP

	AWS :
	https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
	aws eks --region K8S_ZONE update-kubeconfig --name K8S_CLUSTER_NAME

	### TODO : Test this cluster authentication method ###
	Alicloud :
	No documentation 
	aliyun cs DescribeClusterV2UserKubeconfig --ClusterId K8S_CLUSTER_NAME
	"
fi

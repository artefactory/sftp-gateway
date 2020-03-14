#!/bin/sh

source config/${ENV}
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

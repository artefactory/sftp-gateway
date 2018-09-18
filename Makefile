ifndef PROJECT_ID
  $(error PROJECT_ID is undefined)
endif

DOCKER_IMAGE = gcs-sftp-gateway
DOCKER_REGISTRY=eu.gcr.io
DOCKER_TAG=v1

KUBE_SECRET = sftp-credentials
KUBE_CLUSTER_NAME = sftp-gateway
KUBE_ZONE = europe-west3-a
KUBE_SERVICE_ACCOUNT = sftp-gateway

SERVICE_KEYFILE = credentials/key.json
PRIVATE_KEYFILE = credentials/sftp.key
PUBLIC_KEYFILE = ${PRIVATE_KEYFILE}.pub

IAM_ACCOUNT = ${KUBE_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

kubernetes_create_deployment: kubernetes_setup_access
	kubectl create -f kube/pod.yml

kubernetes_create_service: kubernetes_setup_access
	kubectl create -f kube/service.yml

kubernetes_setup_access:
	gcloud --project ${PROJECT_ID} container clusters get-credentials ${KUBE_CLUSTER_NAME} --zone ${KUBE_ZONE}
	account=$$(gcloud info --format='value(config.account)') ; \
	binding_name=$$(echo $$account | cut -d @ -f1 | tr . -)-admin ; \
	$(call create_admin_binding,$$binding_name,--user $$account)

define create_admin_binding
	binding_exists=$$(kubectl get clusterrolebinding -o json | jq -Mr --arg BINDNAME $(1) '.items | map(select(.metadata.name == $$BINDNAME)) | length') ; \
	if [ $$binding_exists -ne 1 ] ; \
	then \
		kubectl create clusterrolebinding $$binding_name $(2) --clusterrole cluster-admin ; \
	fi
endef

kubernetes_gcp_service_account: kubernetes_create_gcp_service_account kubernetes_create_gcp_service_account_key

kubernetes_create_gcp_service_account:
	service_account_exists=$$(gcloud --project ${PROJECT_ID} iam service-accounts list --format json | jq -Mr 'map(select(.displayName=="${KUBE_SERVICE_ACCOUNT}")) | length') ; \
	if [ $$service_account_exists -ne 1 ] ; \
	then \
		gcloud --project ${PROJECT_ID} iam service-accounts create ${KUBE_SERVICE_ACCOUNT} --display-name ${KUBE_SERVICE_ACCOUNT} ; \
	fi

kubernetes_create_gcp_service_account_key: credentials_dir kubernetes_create_gcp_service_account
	gcloud --project ${PROJECT_ID} iam service-accounts keys create ${SERVICE_KEYFILE} --iam-account ${IAM_ACCOUNT} ;\
	keyid=$$(cat ${SERVICE_KEYFILE} | jq -Mr '.private_key_id') ; \
	for key in $$(gcloud --project ${PROJECT_ID} iam service-accounts keys list --iam-account ${IAM_ACCOUNT} --format json | jq -Mr '.[] | .name' | xargs basename) ; do \
			if [ $$key != $$keyid ] ; \
			then \
			gcloud --verbosity=none --quiet --project ${PROJECT_ID} iam service-accounts keys delete $$key --iam-account ${IAM_ACCOUNT} 2>&1 > /dev/null ; \
			fi ; \
	done ; \
	echo "Old keys flushed"

kubernetes_ssh_key: credentials_dir
	if [ -f ${PRIVATE_KEYFILE} ]; \
	then \
		echo "Public key exists, skipping" ; \
	else \
		ssh-keygen -N "" -f ${PRIVATE_KEYFILE} ; \
	fi

kubernetes_upload_secret: kubernetes_setup_access kubernetes_create_gcp_service_account_key kubernetes_ssh_key
	secret_exists=$$(kubectl get secrets -o json | jq -Mr '.items | map(select(.metadata.name=="${KUBE_SECRET}")) | length') ; \
	if [ $$secret_exists -eq 1 ] ; \
	then \
		kubectl delete secrets ${KUBE_SECRET} ; \
	fi
	kubectl create secret generic ${KUBE_SECRET} --from-file=${SERVICE_KEYFILE} --from-file=${PUBLIC_KEYFILE}

credentials_dir:
	mkdir -p credentials

docker_publish: docker_build docker_configure_auth
	docker tag ${DOCKER_IMAGE} ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}
	docker push ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}

docker_configure_auth:
	gcloud --project ${PROJECT_ID} auth configure-docker

docker_build:
	docker build -t ${DOCKER_IMAGE} .

docker_run_test: docker_build
	docker run -a STDIN -a STDERR -a STDOUT -it \
	 					 --mount type=bind,source=$$(pwd)/credentials/,target=/var/secrets/credentials/ \
						 --mount type=bind,source=$$(pwd)/image/opt/,target=/opt/ \
						 --cap-add SYS_ADMIN --device /dev/fuse \
						 --env GCSSFTP_USER=${GCSSFTP_USER} \
						 --env GCSSFTP_BUCKET=${GCSSFTP_BUCKET} \
						 -P \
						 ${DOCKER_IMAGE}

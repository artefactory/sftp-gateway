ifndef ENV
	ENV=dev
endif

ENV_FILE = env/${ENV}

include ${ENV_FILE}

DOCKER_IMAGE = gcs-sftp-gateway
DOCKER_REGISTRY = eu.gcr.io
DOCKER_TAG = v14
DOCKER_URL= ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}

KUBE_APP_LABEL = sftp-gateway-${ENV}
KUBE_SERVICE = sftp-gateway-${ENV}-service

KUBE_SERVICE_ACCOUNT = sftp-gateway-${ENV}
KUBE_CREDENTIALS_SECRET = sftp-gateway-${ENV}-credentials
KUBE_HOSTKEYS_SECRET = sftp-gateway-${ENV}-hostkeys
KUBE_GENERATED_CONFIG_DIR = kube_generated/${ENV}

GCP_SERVICE_ACCOUNT_KEYFILE = credentials/${ENV}/key.json
SSH_PRIVATE_KEYFILE = credentials/${ENV}/sftp.key
SSH_PUBLIC_KEYFILE = ${SSH_PRIVATE_KEYFILE}.pub
SSH_HOST_KEY_DIRECTORY = credentials/${ENV}/hostkeys

GCP_IAM_ACCOUNT = ${KUBE_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

KUBE_PODTEMPLATE = kube/pod.yml.tpl
KUBE_PODFILE = ${KUBE_GENERATED_CONFIG_DIR}/pod.yml

KUBE_SERVICETEMPLATE = kube/service.yml.tpl
KUBE_SERVICEFILE = ${KUBE_GENERATED_CONFIG_DIR}/service.yml



docker_publish: docker_build docker_configure_auth
	docker tag ${DOCKER_IMAGE} ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}
	docker push ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}

docker_configure_auth:
	gcloud --project ${PROJECT_ID} auth configure-docker

docker_build:
	docker build -t ${DOCKER_IMAGE} .

docker_run: docker_build
	docker run -a STDIN -a STDERR -a STDOUT -it \
						 --env-file ${ENV_FILE} \
						 -v $$(pwd)/credentials/${ENV}:/var/secrets/credentials/ \
						 -p 3000:22 \
						 ${DOCKER_IMAGE}

credentials: create_ssh_key create_ssh_host_key create_gcp_service_account_key

create_gcp_service_account:
	service_account_exists=$$(gcloud --project ${PROJECT_ID} iam service-accounts list --format json | jq -Mr 'map(select(.displayName=="${KUBE_SERVICE_ACCOUNT}")) | length') ; \
	if [ $$service_account_exists -ne 1 ] ; \
	then \
		gcloud --project ${PROJECT_ID} iam service-accounts create ${KUBE_SERVICE_ACCOUNT} --display-name ${KUBE_SERVICE_ACCOUNT} ; \
	fi

create_gcp_service_account_key: credentials_dir create_gcp_service_account
	if [ -f ${GCP_SERVICE_ACCOUNT_KEYFILE} ]; \
	then \
	echo "Service account key exists, skipping" ; \
	else \
	gcloud --project ${PROJECT_ID} iam service-accounts keys create ${GCP_SERVICE_ACCOUNT_KEYFILE} --iam-account ${GCP_IAM_ACCOUNT} ;\
	keyid=$$(cat ${GCP_SERVICE_ACCOUNT_KEYFILE} | jq -Mr '.private_key_id') ; \
	for key in $$(gcloud --project ${PROJECT_ID} iam service-accounts keys list --iam-account ${GCP_IAM_ACCOUNT} --format json | jq -Mr '.[] | .name' | xargs basename) ; do \
			if [ $$key != $$keyid ] ; \
			then \
			gcloud --verbosity=none --quiet --project ${PROJECT_ID} iam service-accounts keys delete $$key --iam-account ${GCP_IAM_ACCOUNT} 2>&1 > /dev/null ; \
			fi ; \
	done ; \
	echo "Old keys flushed" ; \
	fi

create_ssh_key: credentials_dir
	if [ -f ${SSH_PUBLIC_KEYFILE} ]; \
	then \
		echo "Public key exists, skipping" ; \
	else \
		ssh-keygen -N "" -f ${SSH_PRIVATE_KEYFILE} ; \
	fi

create_ssh_host_key: credentials_dir
	if [ -d ${SSH_HOST_KEY_DIRECTORY} ]; \
	then \
		echo "SSH Host key directory exists, skipping" ; \
	else \
		mkdir -p ${SSH_HOST_KEY_DIRECTORY} && \
		ssh-keygen -N "" -t ecdsa -f ${SSH_HOST_KEY_DIRECTORY}/ssh_host_ecdsa_key && \
		ssh-keygen -N "" -t dsa -f ${SSH_HOST_KEY_DIRECTORY}/ssh_host_dsa_key && \
		ssh-keygen -N "" -t ed25519 -f ${SSH_HOST_KEY_DIRECTORY}/ssh_host_ed25519_key && \
		ssh-keygen -N "" -t rsa -b 4096 -f ${SSH_HOST_KEY_DIRECTORY}/ssh_host_rsa_key ; \
	fi

credentials_dir:
	mkdir -p credentials/${ENV}


kubernetes_run: docker_publish create_kubernetes_credentials_secret create_kubernetes_hostkeys_secret create_kubernetes_service create_kubernetes_deployment

generate_kubernetes_deployment_file:
	mkdir -p ${KUBE_GENERATED_CONFIG_DIR}
	export $$(cat ${ENV_FILE} | xargs) && \
	DOCKER_URL=${DOCKER_URL} \
	KUBE_APP_LABEL=${KUBE_APP_LABEL} \
	KUBE_CREDENTIALS_SECRET=${KUBE_CREDENTIALS_SECRET} \
	KUBE_HOSTKEYS_SECRET=${KUBE_HOSTKEYS_SECRET} \
	python -c "import pystache; import os; print pystache.render(open('${KUBE_PODTEMPLATE}', 'r').read(), dict(os.environ))" > ${KUBE_PODFILE}

generate_kubernetes_service_file:
	mkdir -p ${KUBE_GENERATED_CONFIG_DIR}
	export $$(cat ${ENV_FILE} | xargs) && \
	KUBE_APP_LABEL=${KUBE_APP_LABEL} \
	KUBE_SERVICE=${KUBE_SERVICE} \
	python -c "import pystache; import os; print pystache.render(open('${KUBE_SERVICETEMPLATE}', 'r').read(), dict(os.environ))" > ${KUBE_SERVICEFILE}

create_kubernetes_deployment: setup_kubernetes_access generate_kubernetes_deployment_file
	kubectl create -f ${KUBE_GENERATED_CONFIG_DIR}/pod.yml

create_kubernetes_service: setup_kubernetes_access generate_kubernetes_service_file
	kubectl create -f ${KUBE_GENERATED_CONFIG_DIR}/service.yml

create_kubernetes_credentials_secret: setup_kubernetes_access credentials
	secret_exists=$$(kubectl get secrets -o=json | jq -Mr '.items | map(select(.metadata.name == "${KUBE_CREDENTIALS_SECRET}")) | length') ; \
	if [ $$secret_exists -eq 1 ] ; \
	then \
		kubectl delete secret ${KUBE_CREDENTIALS_SECRET} ; \
	fi ; \
	kubectl create secret generic ${KUBE_CREDENTIALS_SECRET} --from-file=${GCP_SERVICE_ACCOUNT_KEYFILE} --from-file=${SSH_PUBLIC_KEYFILE} ;

create_kubernetes_hostkeys_secret: setup_kubernetes_access credentials
	secret_exists=$$(kubectl get secrets -o=json | jq -Mr '.items | map(select(.metadata.name == "${KUBE_HOSTKEYS_SECRET}")) | length') ; \
	if [ $$secret_exists -eq 1 ] ; \
	then \
		kubectl delete secret ${KUBE_HOSTKEYS_SECRET} ; \
	fi ; \
	kubectl create secret generic ${KUBE_HOSTKEYS_SECRET} --from-file=${SSH_HOST_KEY_DIRECTORY} ;

setup_kubernetes_access:
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

ifndef PROJECT_ID
  $(error PROJECT_ID is undefined)
endif

ifndef GCSSFTP_USER
  $(error GCSSFTP_USER is undefined)
endif

ifndef GCSSFTP_BUCKET
  $(error GCSSFTP_BUCKET is undefined)
endif

ifndef GCSSFTP_IP
	$(error GCSSFTP_IP is undefined)
endif

DOCKER_IMAGE = gcs-sftp-gateway
DOCKER_REGISTRY = eu.gcr.io
DOCKER_TAG = v2
DOCKER_URL= ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}

KUBE_SECRET = sftp-credentials
KUBE_CLUSTER_NAME = sftp-gateway
KUBE_ZONE = europe-west3-a
KUBE_SERVICE_ACCOUNT = sftp-gateway
KUBE_GENERATED_CONFIG_DIR = kube_generated

GCP_SERVICE_ACCOUNT_KEYFILE = credentials/${PROJECT_ID}/key.json
SSH_PRIVATE_KEYFILE = credentials/${PROJECT_ID}/sftp.key
SSH_PUBLIC_KEYFILE = ${SSH_PRIVATE_KEYFILE}.pub

GCP_IAM_ACCOUNT = ${KUBE_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

KUBE_SECRETTEMPLATE = kube/secret.yml.tpl
KUBE_SECRET = ${KUBE_GENERATED_CONFIG_DIR}/secret.yml

KUBE_PODTEMPLATE = kube/pod.yml.tpl
KUBE_PODFILE = ${KUBE_GENERATED_CONFIG_DIR}/pod.yml

KUBE_SERVICETEMPLATE = kube/service.yml.tpl
KUBE_SERVICEFILE = ${KUBE_GENERATED_CONFIG_DIR}/service.yml

ENV_FILE = env/${PROJECT_ID}

docker_publish: docker_build docker_configure_auth
	docker tag ${DOCKER_IMAGE} ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}
	docker push ${DOCKER_REGISTRY}/${PROJECT_ID}/${DOCKER_IMAGE}:${DOCKER_TAG}

docker_configure_auth:
	gcloud --project ${PROJECT_ID} auth configure-docker

docker_build:
	docker build -t ${DOCKER_IMAGE} .

docker_run: docker_build generate_env_file
	docker run -a STDIN -a STDERR -a STDOUT -it \
						 --env-file ${ENV_FILE} \
						 -p 3000:22 \
						 ${DOCKER_IMAGE}

generate_env_file: credentials
	mkdir -p env
	export GCSSFTP_USER=${GCSSFTP_USER} && \
	export GCSSFTP_BUCKET=${GCSSFTP_BUCKET} && \
	export GCSSFTP_SSH_PUBKEY_FILE=${SSH_PUBLIC_KEYFILE} && \
	export GCSSFTP_SERVICE_ACCOUNT_KEY_FILE=${GCP_SERVICE_ACCOUNT_KEYFILE} && \
	export GCSSFTP_PROJECT_ID=${PROJECT_ID} && \
	python ./bin/generate_env_file.py > ${ENV_FILE}

credentials: create_ssh_key create_gcp_service_account_key

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

credentials_dir:
	mkdir -p credentials/${PROJECT_ID}


kubernetes_run: docker_publish kubernetes_upload_secret create_kubernetes_service create_kubernetes_deployment

generate_kubernetes_deployment_file: generate_env_file
	mkdir -p ${KUBE_GENERATED_CONFIG_DIR}
	DOCKER_URL=${DOCKER_URL} \
	python -c "import pystache; import os; print pystache.render(open('${KUBE_PODTEMPLATE}', 'r').read(), dict(os.environ))" > ${KUBE_PODFILE}

generate_kubernetes_secret_file: generate_env_file
	mkdir -p ${KUBE_GENERATED_CONFIG_DIR}
	export $$(cat ${ENV_FILE} | xargs) && \
	python -c "import pystache; import base64; import os; print pystache.render(open('${KUBE_SECRETTEMPLATE}', 'r').read(), {k: base64.b64encode(v) for k,v in os.environ.iteritems()})" > ${KUBE_SECRET}

generate_kubernetes_service_file:
	mkdir -p ${KUBE_GENERATED_CONFIG_DIR}
	GCSSFTP_IP=${GCSSFTP_IP} \
	python -c "import pystache; import os; print pystache.render(open('${KUBE_SERVICETEMPLATE}', 'r').read(), dict(os.environ))" > ${KUBE_SERVICEFILE}

create_kubernetes_deployment: setup_kubernetes_access generate_kubernetes_deployment_file
	kubectl create -f ${KUBE_GENERATED_CONFIG_DIR}/pod.yml

create_kubernetes_service: setup_kubernetes_access generate_kubernetes_service_file
	kubectl create -f ${KUBE_GENERATED_CONFIG_DIR}/service.yml

create_kubernetes_secret: setup_kubernetes_access generate_kubernetes_secret_file
	kubectl create -f ${KUBE_GENERATED_CONFIG_DIR}/secret.yml

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

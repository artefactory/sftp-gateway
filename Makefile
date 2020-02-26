$(info ENV="$(ENV)")

# Load config values
ifndef ENV
	environment = dev
else
	environment = ${ENV}
endif

# Generate complete config files
ifndef SKIP_CONFIG
	CONFIG := $(shell ENV="$(environment)" SKIP_CONFIG=1 make generate_config)
	GCLOUD_USER=$(shell gcloud config list account --format "value(core.account)")

	ENV_FILE = config/${environment}

	include ${ENV_FILE}
endif


.PHONY: clean
clean:
	find . -name "*pyc" -exec rm -f {} \;

.PHONY: clean_config
clean_config:
	rm -rf config
	rm -rf helm/secrets
	rm -rf helm/values


.PHONY: docker_publish
docker_publish: docker_build docker_configure_auth
	docker tag ${APP_DOCKER_IMAGE} ${APP_DOCKER_REGISTRY}/${GCP_PROJECT_ID}/${APP_DOCKER_IMAGE}:${APP_DOCKER_TAG}
	docker push ${APP_DOCKER_REGISTRY}/${GCP_PROJECT_ID}/${APP_DOCKER_IMAGE}:${APP_DOCKER_TAG}

.PHONY: docker_configure_auth
docker_configure_auth:
	gcloud --project ${GCP_PROJECT_ID} auth configure-docker

.PHONY: docker_build
docker_build: clean generate_config
	build_args=$$(for i in $$(cat ${ENV_FILE}); do out+="--build-arg $${i} " ; done; echo $${out};out="") && \
	docker build --rm -t ${APP_DOCKER_IMAGE} $${build_args} .

.PHONY: docker_run
docker_run: docker_build generate_config credentials
	docker run -a STDIN -a STDERR -a STDOUT -it \
						 --rm \
						 --env-file ${ENV_FILE} \
						 -v $$(pwd)/credentials/${environment}/files:${APP_SECRETS_DIR} \
						 -p ${APP_HOST_PORT}:${APP_SFTP_PORT} \
						${APP_DOCKER_IMAGE}

.PHONY: credentials
credentials: create_ssh_key create_ssh_host_keys create_gcp_service_account_key

.PHONY: create_gcp_service_account
create_gcp_service_account:
	service_account_exists=$$(gcloud --project ${GCP_PROJECT_ID} iam service-accounts list --format json | jq -Mr 'map(select(.displayName=="${GCP_SERVICEACCOUNT_NAME}")) | length') ; \
	if [ $$service_account_exists -ne 1 ] ; \
	then \
		gcloud --project ${GCP_PROJECT_ID} iam service-accounts create ${GCP_SERVICEACCOUNT_NAME} --display-name ${GCP_SERVICEACCOUNT_NAME} ; \
		gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} --member serviceAccount:${GCP_SERVICEACCOUNT_IAM} --role roles/storage.objectAdmin ; \
	fi

GCP_SERVICEACCOUNT_KEY_NAME ?= dummy-service-account
MK_GCP_SERVICEACCOUNT_KEY_NAME = credentials/${environment}/files/${GCP_SERVICEACCOUNT_KEY_NAME}

.PHONY: create_gcp_service_account_key
create_gcp_service_account_key: create_gcp_service_account credentials_dir $(MK_GCP_SERVICEACCOUNT_KEY_NAME)


$(MK_GCP_SERVICEACCOUNT_KEY_NAME):
	gcloud --project ${GCP_PROJECT_ID} iam service-accounts keys create ${MK_GCP_SERVICEACCOUNT_KEY_NAME} --iam-account ${GCP_SERVICEACCOUNT_IAM}

MK_CREDENTIALS_DIR = credentials/${environment}
MK_CREDENTIALS_FILES_DIR = ${MK_CREDENTIALS_DIR}/files
MK_CREDENTIALS_ENV = $(MK_CREDENTIALS_DIR)/env
MK_CREDENTIALS_FILES = $(wildcard $(MK_CREDENTIALS_FILES_DIR)/*)

APP_SFTP_PUBLICKEY_NAME ?= dummy-public-key-value
APP_SFTP_PRIVATEKEY_NAME ?= dummy-private-key-value
MK_APP_SFTP_PUBLICKEY = ${MK_CREDENTIALS_FILES_DIR}/${APP_SFTP_PUBLICKEY_NAME}
MK_APP_SFTP_PRIVATEKEY = ${MK_CREDENTIALS_FILES_DIR}/${APP_SFTP_PRIVATEKEY_NAME}

.PHONY: create_ssh_key
create_ssh_key: credentials_dir $(MK_APP_SFTP_PUBLICKEY)

$(MK_APP_SFTP_PUBLICKEY):
	ssh-keygen -N "" -f ${MK_APP_SFTP_PRIVATEKEY}


MK_APP_SFTP_HOSTKEY_ECDSA = ${MK_CREDENTIALS_FILES_DIR}/ssh_host_ecdsa_key
MK_APP_SFTP_HOSTKEY_DSA = ${MK_CREDENTIALS_FILES_DIR}/ssh_host_dsa_key
MK_APP_SFTP_HOSTKEY_ED25519 = ${MK_CREDENTIALS_FILES_DIR}/ssh_host_ed25519_key
MK_APP_SFTP_HOSTKEY_RSA = ${MK_CREDENTIALS_FILES_DIR}/ssh_host_rsa_key

.PHONY: create_ssh_host_keys
create_ssh_host_keys: credentials_dir $(MK_APP_SFTP_HOSTKEY_ECDSA) $(MK_APP_SFTP_HOSTKEY_DSA) $(MK_APP_SFTP_HOSTKEY_ED25519) $(MK_APP_SFTP_HOSTKEY_RSA)

$(MK_APP_SFTP_HOSTKEY_ECDSA):
	ssh-keygen -N "" -t ecdsa -f $(MK_APP_SFTP_HOSTKEY_ECDSA)

$(MK_APP_SFTP_HOSTKEY_DSA):
	ssh-keygen -N "" -t dsa -f $(MK_APP_SFTP_HOSTKEY_DSA)

$(MK_APP_SFTP_HOSTKEY_ED25519):
	ssh-keygen -N "" -t ed25519 -f $(MK_APP_SFTP_HOSTKEY_ED25519)

$(MK_APP_SFTP_HOSTKEY_RSA):
	ssh-keygen -N "" -t rsa -b 4096 -f $(MK_APP_SFTP_HOSTKEY_RSA)



.PHONY: credentials_dir
credentials_dir: $(MK_CREDENTIALS_DIR) $(MK_CREDENTIALS_FILES_DIR)

$(MK_CREDENTIALS_DIR):
	mkdir -p $(MK_CREDENTIALS_DIR)

$(MK_CREDENTIALS_FILES_DIR):
	mkdir -p $(MK_CREDENTIALS_FILES_DIR)



MK_GENERATED_CONFIG = config/${environment}

.PHONY: generate_config
generate_config: $(MK_GENERATED_CONFIG)

$(MK_GENERATED_CONFIG): env/${environment} env/common
	ENV=${environment} ./bin/configure.sh


MK_HELM_CONFIG = helm/nautilus-sftp-gateway/values/${environment}.yaml
MK_HELM_SECRETS = helm/nautilus-sftp-gateway/secrets/${environment}

.PHONY: helm_generate_values
helm_generate_values: $(MK_HELM_CONFIG) credentials

helm/nautilus-sftp-gateway/values:
	mkdir -p helm/nautilus-sftp-gateway/values

$(MK_HELM_CONFIG): $(MK_GENERATED_CONFIG) $(MK_CREDENTIALS_FILES) helm/nautilus-sftp-gateway/values
	rm -rf $(MK_HELM_SECRETS)
	mkdir -p $(MK_HELM_SECRETS)
	cp $(MK_CREDENTIALS_FILES) $(MK_HELM_SECRETS)
	python ./bin/env_to_values.py --env-file $(MK_GENERATED_CONFIG) > $(MK_HELM_CONFIG)


.PHONY: helm_setup
helm_setup:
	kubectl apply -f helm/rbac-tiller.yaml
	helm init --service-account tiller --upgrade

.PHONY: helm_debug
helm_debug: helm_generate_values
	helm install --dry-run --debug --set gcloud.user=${GCLOUD_USER} -f helm/nautilus-sftp-gateway/values/${environment}.yaml ./helm/nautilus-sftp-gateway

.PHONY: helm_install
helm_install: setup_kubernetes_access docker_publish helm_generate_values
	count=$$(helm ls -q ${APP_NAME} | grep -c "^${APP_NAME}$$"); \
	if [ $${count} -eq 1 ]; then \
		command="upgrade ${APP_NAME} --recreate-pods"; \
	else \
		command="install --name ${APP_NAME}"; \
	fi; \
	helm $${command} --set gcloud.user=${GCLOUD_USER} -f helm/nautilus-sftp-gateway/values/${environment}.yaml ./helm/nautilus-sftp-gateway


.PHONY: setup_kubernetes_access
setup_kubernetes_access:
	gcloud --project ${GCP_PROJECT_ID} container clusters get-credentials ${K8S_CLUSTER_NAME} --zone ${K8S_ZONE}


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

$(info ENV=$(ENV))

# Load config values
ifndef ENV
	environment = dev
else
	environment = ${ENV}
endif

ENV_FILE = config/${environment}.yaml
APP_NAME = $$(cat ${ENV_FILE} | awk '/  NAME:/ {print $$2}')
APP_HOST_PORT = $$(cat ${ENV_FILE} | awk '/HOST_PORT:/ {print $$2}')
APP_SERVICE_PORT = $$(cat ${ENV_FILE} | awk '/SERVICE_PORT:/ {print $$2}')
APP_DOCKER_URL = $$(cat ${ENV_FILE} | awk '/DOCKER_URL:/ {print $$2}')

.PHONY: clean
clean:
	find . -name "*pyc" -exec rm -f {} \;

.PHONY: clean_config
clean_config:
	rm -rf helm/secrets
	rm -rf helm/values

.PHONY: docker_publish
docker_publish: docker_build setup_container_registry_access
	docker push ${APP_DOCKER_URL}

.PHONY: docker_build
docker_build: clean credentials
	docker build --rm -t ${APP_DOCKER_URL} .

.PHONY: docker_run
docker_run: credentials docker_build
	docker run --privileged -a STDIN -a STDERR -a STDOUT -it \
		 --rm \
		 --env ENV=$$(cat ${ENV_FILE} | awk '/ENV:/ {print $$2}') \
		 --env APP_NAME=${APP_NAME} \
		 -v $$(pwd)/credentials/${environment}:/var/run/secrets/${APP_NAME}/ \
		 -v $$(pwd)/config/${environment}.yaml:/var/run/config/${APP_NAME}.yaml \
		 -p ${APP_HOST_PORT}:${APP_SERVICE_PORT} \
		${APP_DOCKER_URL}


MK_CREDENTIALS_ROOT_DIR = credentials
MK_CREDENTIALS_DIR = ${MK_CREDENTIALS_ROOT_DIR}/${environment}
MK_CREDENTIALS_INTERNAL_DIR = ${MK_CREDENTIALS_DIR}/internal
MK_CREDENTIALS_USERS_DIR = ${MK_CREDENTIALS_DIR}/users


.PHONY: create_ssh_keys
create_ssh_keys: credentials_dir create_user_keys


.PHONY: create_user_keys
create_user_keys:
	MK_CREDENTIALS_USERS_DIR=${MK_CREDENTIALS_USERS_DIR} python3 bin/create_user_keys.py


MK_APP_SFTP_HOSTKEY_ECDSA = ${MK_CREDENTIALS_INTERNAL_DIR}/ssh-host-ecdsa-key
MK_APP_SFTP_HOSTKEY_DSA = ${MK_CREDENTIALS_INTERNAL_DIR}/ssh-host-dsa-key
MK_APP_SFTP_HOSTKEY_ED25519 = ${MK_CREDENTIALS_INTERNAL_DIR}/ssh-host-ed25519-key
MK_APP_SFTP_HOSTKEY_RSA = ${MK_CREDENTIALS_INTERNAL_DIR}/ssh-host-rsa-key

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
credentials_dir: $(MK_CREDENTIALS_ROOT_DIR) $(MK_CREDENTIALS_DIR) $(MK_CREDENTIALS_INTERNAL_DIR) $(MK_CREDENTIALS_USERS_DIR)


$(MK_CREDENTIALS_ROOT_DIR):
	mkdir -p $(MK_CREDENTIALS_ROOT_DIR)

$(MK_CREDENTIALS_DIR):
	mkdir -p $(MK_CREDENTIALS_DIR)

$(MK_CREDENTIALS_INTERNAL_DIR):
	mkdir -p $(MK_CREDENTIALS_INTERNAL_DIR)

$(MK_CREDENTIALS_USERS_DIR):
	mkdir -p $(MK_CREDENTIALS_USERS_DIR)


.PHONY: credentials
credentials: create_ssh_host_keys create_ssh_keys create_services_credentials

.PHONY: create_services_credentials
create_services_credentials: create_gcp_service_account_keys create_azure_service_principals create_aws_service_accounts create_alicloud_access_keys

.PHONY: create_gcp_service_accounts
create_gcp_service_account_keys: credentials_dir
	python3 ./bin/create_gcp_service_accounts_and_keys.py

.PHONY: create_azure_service_principals
create_azure_service_principals:
	#TODO

.PHONY: create_aws_access_keys
create_aws_service_accounts:
	python3 ./bin/create_aws_users_and_access_keys.py

.PHONY: create_alicloud_access_keys
    #TODO

MK_CONFIG_DIR = config
MK_CONFIG = ${MK_CONFIG_DIR}/${environment}.yaml

$(MK_CONFIG_DIR):
	mkdir -p $(MK_CONFIG_DIR)

MK_HELM_CONFIG = helm/nautilus-sftp-gateway/values/${environment}.yaml
MK_HELM_SECRETS = helm/nautilus-sftp-gateway/secrets

.PHONY: helm_generate_values
helm_generate_values: credentials $(MK_HELM_CONFIG)

helm/nautilus-sftp-gateway/values:
	mkdir -p helm/nautilus-sftp-gateway/values

$(MK_HELM_CONFIG): $(MK_CONFIG) credentials helm/nautilus-sftp-gateway/values
	rm -rf $(MK_HELM_SECRETS)
	mkdir -p $(MK_HELM_SECRETS)
	cp -r $(MK_CREDENTIALS_DIR) $(MK_HELM_SECRETS)
	cp config/${environment}.yaml $(MK_HELM_CONFIG)

.PHONY: helm_debug
helm_debug: helm_generate_values
	helm install --dry-run --debug ${APP_NAME} -f helm/nautilus-sftp-gateway/values/${environment}.yaml ./helm/nautilus-sftp-gateway

.PHONY: helm_install
helm_install: setup_container_registry_access setup_kubernetes_access docker_publish helm_generate_values
	count=$$(helm ls -q --all-namespaces --filter ${APP_NAME} | grep -c "^${APP_NAME}$$"); \
	if [ $${count} -eq 1 ]; then \
		command="upgrade ${APP_NAME} --recreate-pods"; \
	else \
		command="install ${APP_NAME}"; \
	fi; \
	helm $${command} -f helm/nautilus-sftp-gateway/values/${environment}.yaml ./helm/nautilus-sftp-gateway

.PHONY: setup_container_registry_access
setup_container_registry_access:
	ENV=${environment} sh ./bin/setup_container_registry_access.sh

.PHONY: setup_kubernetes_access
setup_kubernetes_access:
	ENV=${environment} sh ./bin/setup_kubernetes_access.sh


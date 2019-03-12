apiVersion: apps/v1 # for versions before 1.9.0 use apps/v1beta2
kind: Deployment
metadata:
  name: {{KUBE_APP_LABEL}}
spec:
  selector:
    matchLabels:
      app: {{KUBE_APP_LABEL}}
  replicas: 2
  template:
    metadata:
      labels:
        app: {{KUBE_APP_LABEL}}
    spec:
      volumes:
      - name: sftp-gateway-credentials
        secret:
          secretName: {{KUBE_CREDENTIALS_SECRET}}
      - name: sftp-gateway-hostkeys
        secret:
          secretName: {{KUBE_HOSTKEYS_SECRET}}
      containers:
      - name: {{KUBE_APP_LABEL}}
        image: {{DOCKER_URL}}
        imagePullPolicy: Always
        command: ["/opt/run.sh"]
        env:
        - name: PROJECT_ID
          value: {{PROJECT_ID}}
        - name: SFTP_USER
          value: {{SFTP_USER}}
        - name: GCS_BUCKET
          value: {{GCS_BUCKET}}
        volumeMounts:
        - name: sftp-gateway-credentials
          mountPath: /var/secrets/credentials
          readOnly: true
        - name: sftp-gateway-hostkeys
          mountPath: /var/secrets/ssh_host_keys
          readOnly: true
        ports:
        - containerPort: 22

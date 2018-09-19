apiVersion: apps/v1 # for versions before 1.9.0 use apps/v1beta2
kind: Deployment
metadata:
  name: gcs-sftp-gateway
spec:
  selector:
    matchLabels:
      app: gcs-sftp-gateway
  replicas: 2
  template:
    metadata:
      labels:
        app: gcs-sftp-gateway
    spec:
      volumes:
      - name: sftp-credentials
        secret:
          secretName: sftp-credentials
      containers:
      - name: gcs-sftp-gateway
        image: {{DOCKER_URL}}
        imagePullPolicy: Always
        command: ["/opt/run.sh"]
        volumeMounts:
        - name: sftp-credentials
          mountPath: /var/secrets/credentials
        env:
        - name: GCSSFTP_USER
          value: {{GCSSFTP_USER}}
        - name: GCSSFTP_BUCKET
          value: {{GCSSFTP_BUCKET}}
        ports:
        - containerPort: 22
        securityContext:
          privileged: true
          capabilities:
            add:
              - SYS_ADMIN

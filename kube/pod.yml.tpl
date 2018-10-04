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
      containers:
      - name: gcs-sftp-gateway
        image: {{DOCKER_URL}}
        imagePullPolicy: Always
        command: ["/opt/run.sh"]
        envFrom:
        - secretRef:
            name: gcs-sftp-gateway-secret
        ports:
        - containerPort: 22

apiVersion: v1
kind: Service
metadata:
  name: gcs-sftp-gateway-service
  annotations:
    cloud.google.com/load-balancer-type: "Internal"
spec:
  type: LoadBalancer
  loadBalancerIP: {{GCSSFTP_IP}}
  ports:
  - name: sftp
    port: 22
    protocol: TCP
  selector:
    app: gcs-sftp-gateway

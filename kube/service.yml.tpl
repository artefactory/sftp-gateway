apiVersion: v1
kind: Service
metadata:
  name: {{KUBE_SERVICE}}
  {{#INTERNAL}}
  annotations:
    cloud.google.com/load-balancer-type: "Internal"
  {{/INTERNAL}}
spec:
  type: LoadBalancer
  loadBalancerIP: {{SFTP_IP}}
  ports:
  - name: sftp
    port: 22
    protocol: TCP
  selector:
    app: {{KUBE_APP_LABEL}}

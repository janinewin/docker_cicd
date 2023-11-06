### RabbitMQ

RabbitMQ on k8s is very easy with a nice helm chart from bitnami.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install rabbitmq bitnami/rabbitmq
```

If it needs more customization refer to https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq

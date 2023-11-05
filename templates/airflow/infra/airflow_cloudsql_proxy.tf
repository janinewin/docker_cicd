resource "kubernetes_deployment" "airflow_cloudsql_proxy" {
  metadata {
    name = "airflow-cloudsql-proxy"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "airflow-cloudsql-proxy"
      }
    }

    template {
      metadata {
        labels = {
          app = "airflow-cloudsql-proxy"
        }
      }

      spec {
        service_account_name = kubernetes_service_account.airflow_cloudsql_proxy.metadata[0].name
        container {
          name  = "cloudsql-proxy"
          image = "gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.1.0"

          args = [
            "--port=5432",
            "--address=0.0.0.0",
            "${var.project_id}:${var.location}:airflow-data"
          ]

          port {
            container_port = 5432
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "airflow_cloudsql_proxy_svc" {
  metadata {
    name = "cloud-sql-proxy"
  }

  spec {
    selector = {
      app = "airflow-cloudsql-proxy"
    }

    port {
      port        = 5432
      target_port = 5432
    }

    type = "ClusterIP"
  }
}

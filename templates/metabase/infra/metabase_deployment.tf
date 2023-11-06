resource "kubernetes_deployment" "metabase_cloudsql" {
  metadata {
    name = "metabase-cloudsql"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "metabase-cloudsql"
      }
    }

    template {
      metadata {
        labels = {
          app = "metabase-cloudsql"
        }
      }

      spec {
        service_account_name = kubernetes_service_account.metabase_cloudsql_proxy.metadata[0].name

        container {
          name  = "metabase"
          image = "metabase/metabase:v0.46.8"

          port {
            container_port = 3000
          }

          env {
            name  = "MB_DB_TYPE"
            value = "postgres"
          }
          env {
            name = "MB_DB_DBNAME"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.metabase_db_credentials.metadata[0].name
                key  = "dbname"
              }
            }
          }
          env {
            name  = "MB_DB_HOST"
            value = "localhost"
          }
          env {
            name = "MB_DB_PASS"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.metabase_db_credentials.metadata[0].name
                key  = "password"
              }
            }
          }
          env {
            name = "MB_DB_USER"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.metabase_db_credentials.metadata[0].name
                key  = "username"
              }
            }
          }
          env {
            name  = "MB_DB_PORT"
            value = "5433"
          }
        }

        container {
          name  = "cloudsql-proxy"
          image = "gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.1.0"

          args = [
            "--port=5433",
            "${var.project_id}:${var.location}:metabase-data"
          ]
        }
      }
    }
  }
}

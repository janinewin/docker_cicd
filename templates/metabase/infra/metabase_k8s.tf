resource "kubernetes_secret" "metabase_db_credentials" {
  metadata {
    name = "metabase-db-credentials"
  }

  data = {
    username = "metabase_user"
    password = var.metabase_sql_password
    dbname   = "metabase-data"
  }

  type = "Opaque"
}

resource "kubernetes_service_account" "metabase_cloudsql_proxy" {
  metadata {
    name = "metabase-cloudsql-proxy"
    annotations = {
      "iam.gke.io/gcp-service-account" = "${google_service_account.metabase_iam_service_account.email}"
    }
  }
}

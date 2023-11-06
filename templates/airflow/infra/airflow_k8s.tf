resource "kubernetes_secret" "airflow_db_credentials" {
  metadata {
    name = "airflow-db-credentials"
  }

  data = {
    connection = "postgresql://airflow_user:${var.airflow_sql_password}@cloud-sql-proxy:5432/airflow-data"
  }

  type = "Opaque"
}

resource "kubernetes_secret" "git_credentials" {
  metadata {
    name = "git-credentials"
  }
  data = {
    GIT_SYNC_USERNAME = "token"
    GIT_SYNC_PASSWORD = var.git_repo_token
  }
  type = "Opaque"
}


resource "kubernetes_service_account" "airflow_cloudsql_proxy" {
  metadata {
    name = "airflow-cloudsql-proxy"
    annotations = {
      "iam.gke.io/gcp-service-account" = "${google_service_account.airflow_iam_service_account.email}"
    }
  }
}

resource "kubernetes_role" "airflow_executor_role" {
  metadata {
    name      = "airflow-executor-role"
    namespace = "default"
  }

  rule {
    api_groups = ["", "batch", "extensions", "apps"]
    resources  = ["pods", "pods/log", "secrets", "configmaps", "events", "services", "persistentvolumeclaims"]
    verbs      = ["get", "list", "watch", "create", "update", "delete"]
  }
}

resource "kubernetes_role_binding" "airflow_executor_role_binding" {
  metadata {
    name      = "airflow-executor-role-binding"
    namespace = "default"
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.airflow_cloudsql_proxy.metadata[0].name
    namespace = "default"
  }

  role_ref {
    kind      = "Role"
    name      = kubernetes_role.airflow_executor_role.metadata[0].name
    api_group = "rbac.authorization.k8s.io"
  }
}

resource "google_service_account" "airflow_iam_service_account" {
  account_id   = "airflow-service-account"
  display_name = "airflow-service-account"
  project      = var.project_id
}

resource "google_project_iam_member" "airflow_project_iam_member" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.airflow_iam_service_account.email}"
}

resource "google_service_account_iam_member" "airflow_service_account_iam_member" {
  service_account_id = google_service_account.airflow_iam_service_account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[default/${kubernetes_service_account.airflow_cloudsql_proxy.metadata.0.name}]"
}

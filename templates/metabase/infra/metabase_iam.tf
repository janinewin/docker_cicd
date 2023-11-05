resource "google_service_account" "metabase_iam_service_account" {
    account_id   = "metabase-service-account"
    display_name = "metabase-service-account"
    project      = var.project_id
  }

  resource "google_project_iam_member" "metabase_project_iam_member" {
    project = var.project_id
    role    = "roles/cloudsql.client"
    member  = "serviceAccount:${google_service_account.metabase_iam_service_account.email}"
  }

  resource "google_service_account_iam_member" "metabase_service_account_iam_member" {
    service_account_id = google_service_account.metabase_iam_service_account.name
    role               = "roles/iam.workloadIdentityUser"
    member             = "serviceAccount:${var.project_id}.svc.id.goog[default/metabase-cloudsql-proxy]"
  }

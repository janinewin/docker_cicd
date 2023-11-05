resource "google_sql_database_instance" "airflow_sql_instance" {
  name                = "airflow-data"
  region              = var.location
  database_version    = "POSTGRES_13"
  project             = var.project_id
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_user" "airflow_sql_user" {
  name     = "airflow_user"
  instance = google_sql_database_instance.airflow_sql_instance.name
  password = var.airflow_sql_password
  project  = var.project_id
}

resource "google_sql_database" "airflow_sql_database" {
  name     = "airflow-data"
  instance = google_sql_database_instance.airflow_sql_instance.name
  project  = var.project_id
}

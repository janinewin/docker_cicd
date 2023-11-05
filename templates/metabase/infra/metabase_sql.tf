resource "google_sql_database_instance" "metabase_sql_instance" {
  name                = "metabase-data"
  region              = var.location
  database_version    = "POSTGRES_13"
  project             = var.project_id
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_user" "metabase_sql_user" {
  name     = "metabase_user"
  instance = google_sql_database_instance.metabase_sql_instance.name
  password = var.metabase_sql_password
  project  = var.project_id
}

resource "google_sql_database" "metabase_sql_database" {
  name     = "metabase-data"
  instance = google_sql_database_instance.metabase_sql_instance.name
  project  = var.project_id
}

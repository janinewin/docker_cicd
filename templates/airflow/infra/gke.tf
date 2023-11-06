resource "google_container_cluster" "gke_cluster" {
  name                = var.cluster_name
  location            = var.location
  project             = var.project_id
  initial_node_count  = 1
  enable_autopilot    = true
  deletion_protection = false
}

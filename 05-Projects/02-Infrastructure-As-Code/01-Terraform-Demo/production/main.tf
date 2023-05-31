resource "google_storage_bucket" "state-bucket" {
  name          = "${var.project_name}-bucket-tfstate"
  force_destroy = true
  location      = "EU"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
}

module "my-machine" {
  source       = "../modules/vm"
  machine_name = "my-machine"
}

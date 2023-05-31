resource "google_compute_address" "default" {
  name   = "${var.machine_name}-address"
  region = var.region
}

resource "google_compute_instance" "default" {
  name         = "${var.machine_name}-instance"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.disk_image
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.default.address
    }
  }
}

resource "random_string" "token" {
  length           = 108
  special          = true
  numeric          = true
  lower            = true
  upper            = true
  override_special = ":"
}

data "template_file" "master" {
  template = file("./master.sh")
  vars = {
    token                  = random_string.token.result
    external_lb_ip_address = google_compute_address.master.address
  }
}

resource "google_compute_address" "master" {
  name         = "eip-k3s"
  network_tier = "PREMIUM"
}

resource "google_compute_instance" "master" {
  machine_type = var.master_machine_type
  name         = "k3s-master"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      type  = "pd-standard"
      size  = var.disk_size
    }
  }
  tags = ["k3s-master"]

  network_interface {
    subnetwork = google_compute_subnetwork.vpc_subnetwork.name
    access_config {
      nat_ip = google_compute_address.master.address
    }
  }

  metadata = {
    "ssh-keys" : var.ssh_key
  }
  metadata_startup_script = data.template_file.master.rendered
}

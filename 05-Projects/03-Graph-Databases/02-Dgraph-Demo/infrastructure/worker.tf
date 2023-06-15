data "template_file" "worker" {
  template = file("./worker.sh")
  vars = {
    token          = random_string.token.result
    server_address = google_compute_instance.master.network_interface.0.network_ip
  }
}

resource "google_compute_instance" "worker" {
  count        = var.total_node
  machine_type = var.machine_type
  name         = "k3s-worker-${count.index + 1}"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      type  = "pd-standard"
      size  = var.disk_size
    }
  }
  tags = ["k3s-worker"]
  network_interface {
    subnetwork = google_compute_subnetwork.vpc_subnetwork.name
    access_config {
      network_tier = "PREMIUM"
    }
  }
  metadata = {
    "ssh-keys" : var.ssh_key
  }

  metadata_startup_script = data.template_file.worker.rendered
  depends_on              = [google_compute_instance.master]
}

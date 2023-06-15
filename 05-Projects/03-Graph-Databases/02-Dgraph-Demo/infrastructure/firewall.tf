resource "google_compute_firewall" "ssh" {
  name          = "k3s-ssh"
  network       = google_compute_network.vpc.name
  direction     = "INGRESS"
  source_ranges = var.allowed_ips
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  target_tags = ["k3s-master", "k3s-worker"]
}

resource "google_compute_firewall" "internal" {
  name          = "k3s-internal"
  network       = google_compute_network.vpc.name
  direction     = "INGRESS"
  source_ranges = [var.ip_cidr_range]

  allow {
    protocol = "all"
  }
}

resource "google_compute_firewall" "master" {
  name          = "k3s-master"
  network       = google_compute_network.vpc.name
  direction     = "INGRESS"
  source_ranges = var.allowed_ips

  allow {
    protocol = "tcp"
    ports    = ["6443"]
  }
  target_tags = ["k3s-master"]
}

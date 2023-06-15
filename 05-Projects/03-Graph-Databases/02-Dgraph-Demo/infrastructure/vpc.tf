resource "google_compute_network" "vpc" {
  name                    = "k3s-vpc"
  auto_create_subnetworks = "false"
  routing_mode            = "REGIONAL"
}

resource "google_compute_router" "vpc_router" {
  name    = "k3s-router"
  network = google_compute_network.vpc.self_link
}

resource "google_compute_subnetwork" "vpc_subnetwork" {
  name                     = "k3s-subnetwork"
  network                  = google_compute_network.vpc.self_link
  private_ip_google_access = true
  ip_cidr_range            = var.ip_cidr_range

  secondary_ip_range = [
    {
      range_name    = "k3s-second-range"
      ip_cidr_range = var.ip_cidr_second_range
    }
  ]
}

resource "google_compute_router_nat" "vpc_nat" {
  name                               = "k3s-nat"
  router                             = google_compute_router.vpc_router.name
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"

  subnetwork {
    name                    = google_compute_subnetwork.vpc_subnetwork.self_link
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

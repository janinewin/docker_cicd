variable "machine_name" {
  type    = string
  default = "e2-medium"
}

variable "machine_type" {
  type    = string
  default = "e2-medium"
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "zone" {
  type    = string
  default = "europe-west1-b"
}

variable "disk_image" {
  type    = string
  default = "ubuntu-os-cloud/ubuntu-2004-lts"
}

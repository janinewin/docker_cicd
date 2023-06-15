variable "machine_type" {
  type    = string
  default = "e2-medium"
}
variable "master_machine_type" {
  type    = string
  default = "e2-medium"
}
variable "disk_size" {
  type    = number
  default = 50
}
variable "ssh_key" {
  type = string
}
variable "total_node" {
  type    = number
  default = 2
}
variable "ip_cidr_range" {
  type    = string
  default = "10.0.0.0/24"
}
variable "ip_cidr_second_range" {
  type    = string
  default = "10.1.0.0/24"
}
variable "allowed_ips" {
  type    = list(string)
  default = []
}

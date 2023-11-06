resource "kubernetes_service" "metabase_service" {
  metadata {
    name = "metabase-service"
  }

  spec {
    selector = {
      app = "metabase-cloudsql"
    }

    port {
      protocol    = "TCP"
      port        = 80
      target_port = 3000
    }

    type = "LoadBalancer"
  }
}

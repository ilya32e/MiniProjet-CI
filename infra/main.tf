terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "pipeline" {
  name = "financial-pipeline"
}

resource "docker_volume" "rustfs" {
  name = "financial-pipeline-rustfs"
}

resource "docker_container" "rustfs" {
  name    = "financial-pipeline-rustfs"
  image   = "rustfs/rustfs:latest"
  command = ["/data"]
  env = [
    "RUSTFS_ACCESS_KEY=minio",
    "RUSTFS_SECRET_KEY=minio123",
    "RUSTFS_ADDRESS=:9000",
    "RUSTFS_CONSOLE_ADDRESS=:9001",
    "RUSTFS_CONSOLE_ENABLE=true",
  ]
  networks_advanced { name = docker_network.pipeline.name }
  volumes {
    volume_name    = docker_volume.rustfs.name
    container_path = "/data"
  }
  ports {
    internal = 9000
    external = 9010
  }
  ports {
    internal = 9001
    external = 9011
  }
}

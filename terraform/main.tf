# Configuración del Proveedor (Google Cloud)
provider "google" {
  project = "ai-architect-lab-485015" # Tu ID de proyecto actual (o variable)
  region  = "us-central1"
  zone    = "us-central1-a"
}

# 1. Red Privada (VPC)
resource "google_compute_network" "ai_vpc" {
  name = "ai-rag-network"
}

# 2. Firewall (Permitir tráfico)
resource "google_compute_firewall" "allow_web" {
  name    = "allow-streamlit-and-ssh"
  network = google_compute_network.ai_vpc.name

  # Permitimos SSH (22) y Streamlit (8501)
  allow {
    protocol = "tcp"
    ports    = ["22", "8501"]
  }

  # Desde cualquier IP del mundo
  source_ranges = ["0.0.0.0/0"]
}

# 3. Servidor Virtual (Compute Engine VM)
resource "google_compute_instance" "ai_server" {
  name         = "ai-agent-server"
  machine_type = "e2-medium" # 2 vCPU, 4GB RAM (Equilibrado para IA)

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = google_compute_network.ai_vpc.name
    access_config {
      # Esto le asigna una IP pública efímera para acceder
    }
  }

  tags = ["http-server", "https-server"]

  # STARTUP SCRIPT: La magia de la automatización
  # Esto se ejecuta automáticamente cuando Google crea la máquina.
  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "🚀 Iniciando despliegue del AI Architect..."
    
    # 1. Instalar Docker
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose-plugin git
    
    # 2. Clonar el repositorio
    git clone https://github.com/KorbenDallas007/agente-rag-docker.git
    cd agente-rag-docker
    
    # 3. Desplegar la arquitectura
    sudo docker compose up -d
  EOF
}

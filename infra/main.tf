terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
    project = var.project_id
    region = var.region
}

resource "google_cloud_run_service" "default" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.image

        resources {
          limits = {
            memory = "1Gi"
            cpu    = "1"
          }
        }

        env {
          name  = "ENVIRONMENT"
          value = var.env
        }

        env {
          name  = "DB_URL"
          value = var.db_url
        }

        env {
          name  = "JWT_SECRET_KEY"
          value = var.jwt_secret_key
        }

        env {
          name  = "SUPABASE_URL"
          value = var.supabase_url
        }

        env {
          name  = "SUPABASE_ANON_KEY"
          value = var.supabase_anon_key
        }

        env {
          name  = "SUPABASE_SECRET_KEY"
          value = var.supabase_secret_key
        }

        env {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        }

        env {
          name  = "REDIS_URL"
          value = var.redis_url
        }

        env {
          name  = "CRON_SECRET_KEY"
          value = var.cron_secret_key
        }

        env {
          name  = "LANGCHAIN_TRACING_V2"
          value = tostring(var.langchain_tracing_v2)
        }

        env {
          name  = "LANGCHAIN_ENDPOINT"
          value = var.langchain_endpoint
        }

        env {
          name  = "LANGCHAIN_API_KEY"
          value = var.langchain_api_key
        }

        env {
          name  = "LANGCHAIN_PROJECT"
          value = var.langchain_project
        }
        
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.default.name
  location = google_cloud_run_service.default.location
  role   = "roles/run.invoker"
  member = "allUsers"
}

/* 
To deploy the infrastructure, run the following commands in the infra directory:
terraform init
terraform plan
terraform apply 
*/
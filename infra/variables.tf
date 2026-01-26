variable "project_id" {
  description = "Google cloud project id"
  type        = string
}

variable "region" {
  description = "Google cloud region (ej: us-central1)"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud run service name"
  type        = string
}

variable "image" {
  description = "Docker image url"
  type        = string
}

variable "env" {
  description = "Environment name (dev, prod, etc)"
  type        = string
  default     = "dev"
}

variable "db_url" {
  description = "Database connection url"
  type        = string
}

variable "jwt_secret_key" {
  description = "JWT secret key for token generation"
  type        = string
}

variable "supabase_url" {
  description = "Supabase project url"
  type        = string
}

variable "supabase_anon_key" {
  description = "Supabase anon public key"
  type        = string
}

variable "supabase_secret_key" {
  description = "Supabase service role key"
  type        = string
}

variable "openai_api_key" {
  description = "OpenAI api key"
  type        = string
  default     = ""
}

variable "redis_url" {
  description = "Redis connection url"
  type        = string
  default     = ""
}

variable "cron_secret_key" {
  description = "Secret key for cron job authentication"
  type        = string
  default     = ""
}

variable "langchain_tracing_v2" {
  description = "Enable Langchain Tracing V2"
  type        = bool
  default     = false
}

variable "langchain_endpoint" {
  description = "Langchain Tracing V2 endpoint"
  type        = string
  default     = ""
}

variable "langchain_api_key" {
  description = "Langchain Tracing V2 API key"
  type        = string
  default     = ""
}

variable "langchain_project" {
  description = "Langchain Tracing V2 project name"
  type        = string
  default     = ""
}

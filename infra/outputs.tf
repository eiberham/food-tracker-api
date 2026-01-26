output "service_url" {
  description = "Public url of the cloud run service"
  value       = google_cloud_run_service.default.status[0].url
}
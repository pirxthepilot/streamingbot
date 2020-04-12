variable "region" {
  default = "us-west-2"
}

variable "twitch_client_id" {
  type        = string
  description = "Twitch client ID to use - set in a .tfvars file"
}

variable "slack_webhook_url" {
  type        = string
  description = "Slack webhook URL - set in a .tfvars file"
}

variable "twitch_user" {
  type        = string
  description = "Twitch user to watch - set in a .tfvars file"
}

variable "lambda_package" {
  type        = string
  description = "Path to the zipped lambda package file"
}

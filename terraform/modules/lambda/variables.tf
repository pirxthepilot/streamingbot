/*
*  Instance name
*/

variable name {}


/*
*  Other vars
*/

variable "filename" {
  type        = string
  default     = null
  description = "Path to lambda function zip package (required)"
}

variable "handler" {
  type        = string
  default     = null
  description = "The function entrypoint in the code (required)"
}

variable "runtime" {
  type        = string
  default     = "python3.7"
  description = "The lambda runtime (defaults to python3.7)"
}

variable "description" {
  type        = string
  default     = null
  description = "Description for the lambda function (optional)"
}

variable "custom_role_policy" {
  type        = string
  default     = null
  description = "Role policies specific to the lambda's purpose"
}

variable "envvars" {
  type        = map
  default     = null
  description = "Environment variables"
}

variable "timeout" {
  type        = number
  default     = 3
  description = "Lambda execution timeout"
}

variable "tags" {
  type        = map
  default     = null
  description = "Tags"
}

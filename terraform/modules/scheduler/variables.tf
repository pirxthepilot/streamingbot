/*
*  Instance name
*/

variable name {}


/*
*  Other vars
*/
variable "lambda_function_arn" {
  type        = string
  default     = null
  description = "Lambda ARN that should be triggered by the Cloudwatch rule"
}

variable "schedule_expression" {
  type        = string
  default     = null
  description = "Schedule expression"
}

variable "description" {
  type        = string
  default     = ""
  description = "The description of the rule"
}

variable "is_enabled" {
  type        = bool
  default     = false
  description = "Enable or disable the scheduler"
}

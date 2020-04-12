provider "aws" {
  profile = "default"
  region  = var.region
}

resource "aws_dynamodb_table" "streamingbot" {
  name           = "streamingbotdb"
  hash_key       = "stream_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "stream_id"
    type = "N"
  }

  tags = {
    Name = "streamingbot"
  }
}

module "streamingbot_lambda" {
  source      = "./modules/lambda"
  name        = "streamingbot"
  description = "Twitch stream notifier for Slack"

  filename = var.lambda_package
  handler  = "bot.lambda_handler"
  runtime  = "python3.7"
  timeout  = 30

  envvars = {
    TWITCH_CLIENT_ID  = var.twitch_client_id
    SLACK_WEBHOOK_URL = var.slack_webhook_url
    TWITCH_USER       = var.twitch_user
  }

  custom_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "dynamodb:BatchGetItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:BatchWriteItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "${aws_dynamodb_table.streamingbot.arn}",
      "Effect": "Allow"
    }
  ]
}
POLICY

  tags = {
    Name = "streamingbot"
  }

}

module "lambda_schedule" {
  source      = "./modules/scheduler"
  name        = "streamingbot-schedule"
  description = "Run streamingbot on a cron schedule"
  is_enabled  = true

  lambda_function_arn = module.streamingbot_lambda.lambda_function_arn
  schedule_expression = "rate(${var.run_frequency} minutes)"
}

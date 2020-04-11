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

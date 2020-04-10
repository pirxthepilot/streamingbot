output dynamodb_table_id {
  value = aws_dynamodb_table.streamingbot.id
}

output dynamodb_table_arn {
  value = aws_dynamodb_table.streamingbot.arn
}

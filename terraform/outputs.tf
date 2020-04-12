output lambda_function_arn {
  value = module.streamingbot_lambda.lambda_function_arn
}

output dynamodb_table_arn {
  value = aws_dynamodb_table.streamingbot.arn
}

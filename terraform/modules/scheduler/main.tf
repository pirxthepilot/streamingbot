#
# Lambda scheduler
#

resource "aws_cloudwatch_event_rule" "lambda" {
  name_prefix         = "${var.name}-"
  schedule_expression = var.schedule_expression
  description         = var.description
  is_enabled          = var.is_enabled
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.lambda.name
  arn  = var.lambda_function_arn
}

resource "aws_lambda_permission" "cloudwatch" {
  function_name = var.lambda_function_arn
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda.arn
}

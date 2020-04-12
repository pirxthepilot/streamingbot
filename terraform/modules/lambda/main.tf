/*
*  The Lambda function
*/

resource "aws_lambda_function" "lambda" {
  function_name = var.name
  filename      = var.filename
  handler       = var.handler
  runtime       = var.runtime
  role          = aws_iam_role.lambda.arn
  description   = var.description
  timeout       = var.timeout

  source_code_hash = filebase64sha256("${var.filename}")

  environment {
    variables = var.envvars
  }

  tags = var.tags

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_logging,
    aws_iam_role_policy_attachment.lambda_custom
  ]
}


/*
*  Cloudwatch log group
*/

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = 5
}


/*
*  IAM
*/

resource "aws_iam_role" "lambda" {
  name_prefix = "${var.name}-"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}


# IAM policy for logging to Cloudwatch

resource "aws_iam_policy" "lambda_logging" {
  name_prefix = "${var.name}-logging-"
  description = "IAM policy for logging from a lambda"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "${aws_cloudwatch_log_group.lambda.arn}",
      "Effect": "Allow"
    },
    {
      "Action": [
        "logs:CreateLogGroup"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}


# IAM policy specific to the lambda's purpose

resource "aws_iam_policy" "lambda_custom" {
  #count = var.custom_role_policy == null ? 0 : 1

  name_prefix = "${var.name}-custom-"
  description = "Custom lambda policy"

  policy = var.custom_role_policy
}

resource "aws_iam_role_policy_attachment" "lambda_custom" {
  #count = var.custom_role_policy == null ? 0 : 1

  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_custom.arn
  #policy_arn = aws_iam_policy.lambda_custom[count.index].arn
}

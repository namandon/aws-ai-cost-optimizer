# Lambda Functions Configuration
# Defines both Cost Analyzer and AI Recommender functions

# ============================================
# IAM Role for Lambda Functions
# ============================================

resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

# Basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy for Lambda to access AWS services
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeVolumes",
          "ec2:DescribeSnapshots",
          "ec2:DescribeRegions"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:UpdateItem"
        ]
        Resource = [
          aws_dynamodb_table.cost_data.arn,
          "${aws_dynamodb_table.cost_data.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.reports.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.notifications.arn
      }
    ]
  })
}

# ============================================
# Cost Analyzer Lambda Function
# ============================================

# Package the Lambda function code
data "archive_file" "cost_analyzer" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/cost_analyzer"
  output_path = "${path.module}/cost_analyzer.zip"
}

resource "aws_lambda_function" "cost_analyzer" {
  filename      = data.archive_file.cost_analyzer.output_path
  function_name = local.cost_analyzer_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  source_code_hash = data.archive_file.cost_analyzer.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE              = aws_dynamodb_table.cost_data.name
      S3_BUCKET                   = aws_s3_bucket.reports.id
      SNS_TOPIC_ARN              = aws_sns_topic.notifications.arn
      ENABLE_EMAIL_NOTIFICATIONS = var.enable_email_notifications
      ENABLE_S3_REPORTS          = var.enable_s3_reports
      ENABLE_DETAILED_LOGGING    = var.enable_detailed_logging
      COST_THRESHOLD_WARNING     = var.cost_threshold_warning
      COST_THRESHOLD_CRITICAL    = var.cost_threshold_critical
    }
  }

  tags = merge(
    local.common_tags,
    {
      Name = local.cost_analyzer_name
      Type = "Lambda"
    }
  )
}

# CloudWatch Log Group for Cost Analyzer
resource "aws_cloudwatch_log_group" "cost_analyzer" {
  name              = "/aws/lambda/${aws_lambda_function.cost_analyzer.function_name}"
  retention_in_days = 7

  tags = local.common_tags
}

# ============================================
# AI Recommender Lambda Function
# ============================================

# Package the Lambda function code
data "archive_file" "ai_recommender" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/ai_recommender"
  output_path = "${path.module}/ai_recommender.zip"
}

resource "aws_lambda_function" "ai_recommender" {
  filename      = data.archive_file.ai_recommender.output_path
  function_name = local.ai_recommender_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  source_code_hash = data.archive_file.ai_recommender.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE              = aws_dynamodb_table.cost_data.name
      S3_BUCKET                   = aws_s3_bucket.reports.id
      SNS_TOPIC_ARN              = aws_sns_topic.notifications.arn
      AI_PROVIDER                = var.ai_provider
      AI_MODEL                   = var.ai_model
      AI_TEMPERATURE             = var.ai_temperature
      AI_MAX_TOKENS              = var.ai_max_tokens
      GROQ_API_KEY              = var.groq_api_key
      OPENROUTER_API_KEY        = var.openrouter_api_key
      OLLAMA_HOST               = var.ollama_host
      ENABLE_EMAIL_NOTIFICATIONS = var.enable_email_notifications
      ENABLE_S3_REPORTS          = var.enable_s3_reports
    }
  }

  tags = merge(
    local.common_tags,
    {
      Name = local.ai_recommender_name
      Type = "Lambda"
    }
  )
}

# CloudWatch Log Group for AI Recommender
resource "aws_cloudwatch_log_group" "ai_recommender" {
  name              = "/aws/lambda/${aws_lambda_function.ai_recommender.function_name}"
  retention_in_days = 7

  tags = local.common_tags
}
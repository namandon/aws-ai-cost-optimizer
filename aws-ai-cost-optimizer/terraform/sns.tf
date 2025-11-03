# SNS Topic for Cost Optimization Notifications
# Sends email alerts with reports

resource "aws_sns_topic" "notifications" {
  name = "${var.project_name}-notifications"

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-notifications"
      Type = "SNS"
    }
  )
}

# Email subscription
resource "aws_sns_topic_subscription" "email" {
  count = var.enable_email_notifications ? 1 : 0

  topic_arn = aws_sns_topic.notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# SNS Topic Policy to allow Lambda to publish
resource "aws_sns_topic_policy" "notifications" {
  arn = aws_sns_topic.notifications.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowLambdaPublish"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = [
          "SNS:Publish"
        ]
        Resource = aws_sns_topic.notifications.arn
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })
}
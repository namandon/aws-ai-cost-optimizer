# DynamoDB Table for Cost Optimization Data
# Stores analysis results and recommendations

resource "aws_dynamodb_table" "cost_data" {
  name           = "${var.project_name}-data"
  billing_mode   = var.dynamodb_billing_mode
  hash_key       = "id"
  
  # Only needed if using PROVISIONED billing mode
  read_capacity  = var.dynamodb_billing_mode == "PROVISIONED" ? 5 : null
  write_capacity = var.dynamodb_billing_mode == "PROVISIONED" ? 5 : null

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  # Global Secondary Index for querying by timestamp
  global_secondary_index {
    name            = "TimestampIndex"
    hash_key        = "timestamp"
    projection_type = "ALL"
    
    # Only needed if using PROVISIONED billing mode
    read_capacity  = var.dynamodb_billing_mode == "PROVISIONED" ? 5 : null
    write_capacity = var.dynamodb_billing_mode == "PROVISIONED" ? 5 : null
  }

  # Enable point-in-time recovery (optional but recommended)
  point_in_time_recovery {
    enabled = false  # Set to true for production
  }

  # Server-side encryption
  server_side_encryption {
    enabled = true
  }

  # TTL for automatic data expiration (optional)
  ttl {
    attribute_name = "expiration_time"
    enabled        = true
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-data"
      Type = "DynamoDB"
    }
  )
}

# CloudWatch Alarms for DynamoDB (optional but recommended)
resource "aws_cloudwatch_metric_alarm" "dynamodb_read_throttle" {
  alarm_name          = "${var.project_name}-dynamodb-read-throttle"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ReadThrottleEvents"
  namespace           = "AWS/DynamoDB"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "DynamoDB read throttle events"
  treat_missing_data  = "notBreaching"

  dimensions = {
    TableName = aws_dynamodb_table.cost_data.name
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_metric_alarm" "dynamodb_write_throttle" {
  alarm_name          = "${var.project_name}-dynamodb-write-throttle"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "WriteThrottleEvents"
  namespace           = "AWS/DynamoDB"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "DynamoDB write throttle events"
  treat_missing_data  = "notBreaching"

  dimensions = {
    TableName = aws_dynamodb_table.cost_data.name
  }

  tags = local.common_tags
}
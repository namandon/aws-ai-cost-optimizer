# AWS Cost Optimizer - Outputs
# Display important information after deployment

output "cost_analyzer_function_name" {
  description = "Name of the Cost Analyzer Lambda function"
  value       = aws_lambda_function.cost_analyzer.function_name
}

output "cost_analyzer_function_arn" {
  description = "ARN of the Cost Analyzer Lambda function"
  value       = aws_lambda_function.cost_analyzer.arn
}

output "ai_recommender_function_name" {
  description = "Name of the AI Recommender Lambda function"
  value       = aws_lambda_function.ai_recommender.function_name
}

output "ai_recommender_function_arn" {
  description = "ARN of the AI Recommender Lambda function"
  value       = aws_lambda_function.ai_recommender.arn
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.cost_data.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.cost_data.arn
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for reports"
  value       = aws_s3_bucket.reports.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.reports.arn
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for notifications"
  value       = aws_sns_topic.notifications.arn
}

output "eventbridge_rule_name" {
  description = "Name of the EventBridge schedule rule"
  value       = aws_cloudwatch_event_rule.schedule.name
}

output "schedule_expression" {
  description = "Schedule expression for the cost analyzer"
  value       = var.schedule_expression
}

output "deployment_region" {
  description = "AWS region where resources are deployed"
  value       = var.aws_region
}

output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

# Instructions for the user
output "next_steps" {
  description = "Next steps after deployment"
  value = <<-EOT
  
  ========================================
  🎉 AWS Cost Optimizer Deployed Successfully!
  ========================================
  
  📋 NEXT STEPS:
  
  1. Confirm SNS subscription:
     Check your email (${var.notification_email}) and confirm the subscription
  
  2. Test the Cost Analyzer manually:
     aws lambda invoke --function-name ${aws_lambda_function.cost_analyzer.function_name} response.json
  
  3. View CloudWatch Logs:
     aws logs tail /aws/lambda/${aws_lambda_function.cost_analyzer.function_name} --follow
  
  4. Check DynamoDB table:
     aws dynamodb scan --table-name ${aws_dynamodb_table.cost_data.name}
  
  5. View S3 reports:
     aws s3 ls s3://${aws_s3_bucket.reports.id}/reports/
  
  📊 Scheduled Run: ${var.schedule_expression}
  
  🔧 To destroy all resources:
     terraform destroy -auto-approve
  
  ========================================
  EOT
}
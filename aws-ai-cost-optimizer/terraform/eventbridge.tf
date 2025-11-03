# EventBridge Rule for Scheduled Cost Analysis
# Triggers the cost analyzer Lambda on a schedule

resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.project_name}-schedule"
  description         = "Trigger cost analysis on schedule"
  schedule_expression = var.schedule_expression

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-schedule"
      Type = "EventBridge"
    }
  )
}

# Target: Cost Analyzer Lambda
resource "aws_cloudwatch_event_target" "cost_analyzer" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "CostAnalyzerLambda"
  arn       = aws_lambda_function.cost_analyzer.arn
}

# Permission for EventBridge to invoke Cost Analyzer Lambda
resource "aws_lambda_permission" "allow_eventbridge_cost_analyzer" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cost_analyzer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}

# EventBridge Rule to trigger AI Recommender after Cost Analyzer completes
resource "aws_cloudwatch_event_rule" "cost_analyzer_success" {
  name        = "${var.project_name}-analyzer-success"
  description = "Trigger AI recommender after cost analyzer completes"

  event_pattern = jsonencode({
    source      = ["aws.lambda"]
    detail-type = ["Lambda Function Invocation Result - Success"]
    detail = {
      functionName = [aws_lambda_function.cost_analyzer.function_name]
    }
  })

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-analyzer-success"
      Type = "EventBridge"
    }
  )
}

# Target: AI Recommender Lambda
resource "aws_cloudwatch_event_target" "ai_recommender" {
  rule      = aws_cloudwatch_event_rule.cost_analyzer_success.name
  target_id = "AIRecommenderLambda"
  arn       = aws_lambda_function.ai_recommender.arn
}

# Permission for EventBridge to invoke AI Recommender Lambda
resource "aws_lambda_permission" "allow_eventbridge_ai_recommender" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ai_recommender.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cost_analyzer_success.arn
}
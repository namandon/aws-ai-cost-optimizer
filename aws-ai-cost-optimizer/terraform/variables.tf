# AWS Cost Optimizer - Variables
# Define all configurable parameters

# General Configuration
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "aws-ai-cost-optimizer"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, production)"
  type        = string
  default     = "production"
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = "CloudEngineer"
}

# AWS Configuration
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

# Notification Configuration
variable "notification_email" {
  description = "Email address for cost optimization notifications"
  type        = string
}

variable "enable_email_notifications" {
  description = "Enable email notifications via SNS"
  type        = bool
  default     = true
}

variable "enable_s3_reports" {
  description = "Enable saving reports to S3"
  type        = bool
  default     = true
}

# AI Provider Configuration
variable "ai_provider" {
  description = "AI provider to use (groq, openrouter, ollama)"
  type        = string
  default     = "groq"
  
  validation {
    condition     = contains(["groq", "openrouter", "ollama"], var.ai_provider)
    error_message = "AI provider must be one of: groq, openrouter, ollama"
  }
}

variable "ai_model" {
  description = "AI model to use for generating reports"
  type        = string
  default     = "llama-3.1-70b-versatile"
}

variable "ai_temperature" {
  description = "AI temperature for response generation (0.0-1.0)"
  type        = number
  default     = 0.7
  
  validation {
    condition     = var.ai_temperature >= 0 && var.ai_temperature <= 1
    error_message = "AI temperature must be between 0.0 and 1.0"
  }
}

variable "ai_max_tokens" {
  description = "Maximum tokens for AI response"
  type        = number
  default     = 2000
}

# Groq Configuration
variable "groq_api_key" {
  description = "Groq API key (optional - for Groq provider)"
  type        = string
  default     = ""
  sensitive   = true
}

# OpenRouter Configuration
variable "openrouter_api_key" {
  description = "OpenRouter API key (optional - for OpenRouter provider)"
  type        = string
  default     = ""
  sensitive   = true
}

# Ollama Configuration
variable "ollama_host" {
  description = "Ollama host URL (optional - for Ollama provider)"
  type        = string
  default     = "http://localhost:11434"
}

# Schedule Configuration
variable "schedule_expression" {
  description = "EventBridge schedule expression (cron or rate)"
  type        = string
  default     = "cron(0 9 ? * MON *)"  # Every Monday at 9 AM UTC
}

# Lambda Configuration
variable "lambda_memory_size" {
  description = "Memory size for Lambda functions (MB)"
  type        = number
  default     = 512
  
  validation {
    condition     = var.lambda_memory_size >= 128 && var.lambda_memory_size <= 10240
    error_message = "Lambda memory must be between 128 and 10240 MB"
  }
}

variable "lambda_timeout" {
  description = "Timeout for Lambda functions (seconds)"
  type        = number
  default     = 300
  
  validation {
    condition     = var.lambda_timeout >= 3 && var.lambda_timeout <= 900
    error_message = "Lambda timeout must be between 3 and 900 seconds"
  }
}

# DynamoDB Configuration
variable "dynamodb_billing_mode" {
  description = "DynamoDB billing mode (PROVISIONED or PAY_PER_REQUEST)"
  type        = string
  default     = "PAY_PER_REQUEST"
  
  validation {
    condition     = contains(["PROVISIONED", "PAY_PER_REQUEST"], var.dynamodb_billing_mode)
    error_message = "DynamoDB billing mode must be PROVISIONED or PAY_PER_REQUEST"
  }
}

# Cost Thresholds
variable "cost_threshold_warning" {
  description = "Cost threshold for warning alerts (USD)"
  type        = number
  default     = 100
}

variable "cost_threshold_critical" {
  description = "Cost threshold for critical alerts (USD)"
  type        = number
  default     = 500
}

# Data Retention
variable "report_retention_days" {
  description = "Number of days to retain reports in S3"
  type        = number
  default     = 30
}

variable "metrics_retention_days" {
  description = "Number of days to retain metrics in DynamoDB"
  type        = number
  default     = 90
}

# Feature Flags
variable "enable_detailed_logging" {
  description = "Enable detailed CloudWatch logging"
  type        = bool
  default     = false
}
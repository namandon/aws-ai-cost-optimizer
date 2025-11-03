#!/bin/bash
# AWS Cost Optimizer - Setup Script
# This script helps you set up and deploy the project

set -e  # Exit on any error

echo "========================================="
echo "AWS Cost Optimizer - Setup Script"
echo "========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi
echo "✅ AWS CLI found"

# Check Terraform
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install it first."
    exit 1
fi
echo "✅ Terraform found"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi
echo "✅ Python 3 found"

# Check AWS credentials
echo ""
echo "Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi

AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
echo "✅ AWS Account: $AWS_ACCOUNT"
echo "✅ AWS Region: $AWS_REGION"

# Check if terraform.tfvars exists
echo ""
if [ ! -f "terraform/terraform.tfvars" ]; then
    echo "⚠️  terraform.tfvars not found!"
    echo "Please create terraform/terraform.tfvars with your configuration."
    exit 1
fi
echo "✅ terraform.tfvars found"

# Navigate to terraform directory
cd terraform

# Initialize Terraform
echo ""
echo "Initializing Terraform..."
terraform init

# Validate configuration
echo ""
echo "Validating Terraform configuration..."
terraform validate

# Show what will be created
echo ""
echo "========================================="
echo "Ready to deploy!"
echo "========================================="
echo ""
echo "The following resources will be created:"
echo "  - 2 Lambda functions (Cost Analyzer + AI Recommender)"
echo "  - 1 DynamoDB table"
echo "  - 1 S3 bucket"
echo "  - 1 SNS topic"
echo "  - 2 EventBridge rules"
echo "  - IAM roles and policies"
echo ""
echo "Estimated monthly cost: \$0-3 (mostly FREE tier)"
echo ""
echo "To deploy, run:"
echo "  cd terraform"
echo "  terraform plan    # Review changes"
echo "  terraform apply   # Deploy"
echo ""
echo "========================================="
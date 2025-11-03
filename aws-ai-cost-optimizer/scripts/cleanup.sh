#!/bin/bash
# AWS Cost Optimizer - Cleanup Script
# This script safely destroys all AWS resources

set -e  # Exit on any error

echo "========================================="
echo "AWS Cost Optimizer - Cleanup Script"
echo "========================================="
echo ""
echo "⚠️  WARNING: This will DESTROY all resources!"
echo ""
echo "This includes:"
echo "  - Lambda functions"
echo "  - DynamoDB table (all data will be lost)"
echo "  - S3 bucket (all reports will be deleted)"
echo "  - SNS topic"
echo "  - EventBridge rules"
echo "  - IAM roles"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Starting cleanup..."

# Navigate to terraform directory
cd terraform

# Destroy all resources
echo ""
echo "Destroying AWS resources..."
terraform destroy -auto-approve

echo ""
echo "========================================="
echo "✅ Cleanup complete!"
echo "========================================="
echo ""
echo "All AWS resources have been destroyed."
echo "Your AWS account should no longer incur charges from this project."
echo ""
"""
AI Recommender Lambda Function
Generates cost optimization reports using AI
"""

import json
import boto3
import os
from datetime import datetime
from typing import Dict, Any
from ai_client import AIClient
from prompt_templates import get_cost_analysis_prompt

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
s3 = boto3.client('s3')

# Get environment variables
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'cost-optimizer-data')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
S3_BUCKET = os.environ.get('S3_BUCKET', '')
ENABLE_EMAIL = os.environ.get('ENABLE_EMAIL_NOTIFICATIONS', 'true').lower() == 'true'
ENABLE_S3 = os.environ.get('ENABLE_S3_REPORTS', 'true').lower() == 'true'


def lambda_handler(event, context):
    """
    Main Lambda handler function
    Triggered after cost_analyzer completes
    """
    print("Starting AI recommendation generation...")
    
    try:
        # Step 1: Get latest analysis from DynamoDB
        latest_analysis = get_latest_analysis()
        
        if not latest_analysis:
            print("No analysis data found in DynamoDB")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No analysis data found'})
            }
        
        # Step 2: Generate AI report
        ai_report = generate_ai_report(latest_analysis)
        
        # Step 3: Save report to S3 (optional)
        if ENABLE_S3 and S3_BUCKET:
            save_to_s3(ai_report)
        
        # Step 4: Send email notification (optional)
        if ENABLE_EMAIL and SNS_TOPIC_ARN:
            send_notification(ai_report)
        
        # Step 5: Update DynamoDB with report
        update_analysis_with_report(latest_analysis['id'], ai_report)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'AI report generated successfully',
                'timestamp': datetime.now().isoformat(),
                'report_length': len(ai_report)
            })
        }
        
    except Exception as e:
        print(f"Error generating AI recommendations: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def get_latest_analysis() -> Dict[str, Any]:
    """
    Retrieve the most recent analysis from DynamoDB
    """
    print(f"Fetching latest analysis from DynamoDB table: {TABLE_NAME}")
    
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        # Scan to get all items (in production, use better indexing)
        response = table.scan(
            Limit=10,
            ProjectionExpression='id, #ts, #data, recommendations_count',
            ExpressionAttributeNames={
                '#ts': 'timestamp',
                '#data': 'data'
            }
        )
        
        items = response.get('Items', [])
        
        if not items:
            return None
        
        # Sort by timestamp and get latest
        sorted_items = sorted(items, key=lambda x: x['timestamp'], reverse=True)
        latest = sorted_items[0]
        
        # Parse the JSON data
        latest['data'] = json.loads(latest['data'])
        
        print(f"Found analysis from {latest['timestamp']}")
        return latest
        
    except Exception as e:
        print(f"Error fetching from DynamoDB: {str(e)}")
        return None


def generate_ai_report(analysis_data: Dict[str, Any]) -> str:
    """
    Generate cost optimization report using AI
    """
    print("Generating AI report...")
    
    try:
        # Extract the analysis data
        data = analysis_data['data']
        
        # Initialize AI client
        ai_client = AIClient()
        
        # Generate report using AI
        report = ai_client.generate_report(data)
        
        print(f"AI report generated ({len(report)} characters)")
        return report
        
    except Exception as e:
        print(f"Error generating AI report: {str(e)}")
        # Return fallback report
        return generate_fallback_report(analysis_data)


def generate_fallback_report(analysis_data: Dict[str, Any]) -> str:
    """
    Generate a basic report without AI (fallback)
    """
    data = analysis_data['data']
    recommendations = data.get('recommendations', [])
    total_savings = data.get('total_potential_savings', 0)
    
    report = f"""
═══════════════════════════════════════════════════════════
 AWS COST OPTIMIZATION REPORT
 {datetime.now().strftime('%B %d, %Y')}
═══════════════════════════════════════════════════════════

💰 POTENTIAL MONTHLY SAVINGS: ${total_savings:.2f}

📊 RECOMMENDATIONS FOUND: {len(recommendations)}

"""
    
    if recommendations:
        report += "🎯 TOP RECOMMENDATIONS:\n\n"
        for idx, rec in enumerate(recommendations[:5], 1):
            report += f"{idx}. {rec.get('type', 'Unknown').upper()}\n"
            report += f"   Resource: {rec.get('resource_id', 'N/A')}\n"
            report += f"   Savings: ${rec.get('estimated_savings', 0):.2f}/month\n"
            report += f"   {rec.get('message', 'No details')}\n\n"
    else:
        report += "✅ No optimization opportunities found at this time.\n"
        report += "Your infrastructure appears well-optimized!\n\n"
    
    report += """
═══════════════════════════════════════════════════════════
Next analysis: Next scheduled run
═══════════════════════════════════════════════════════════
"""
    
    return report


def save_to_s3(report: str) -> None:
    """
    Save report to S3 bucket
    """
    if not S3_BUCKET:
        print("S3 bucket not configured, skipping save")
        return
    
    print(f"Saving report to S3 bucket: {S3_BUCKET}")
    
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        key = f"reports/cost-report_{timestamp}.txt"
        
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=report.encode('utf-8'),
            ContentType='text/plain'
        )
        
        print(f"Report saved to s3://{S3_BUCKET}/{key}")
        
    except Exception as e:
        print(f"Error saving to S3: {str(e)}")


def send_notification(report: str) -> None:
    """
    Send report via SNS (email)
    """
    if not SNS_TOPIC_ARN:
        print("SNS topic not configured, skipping notification")
        return
    
    print(f"Sending notification to SNS topic: {SNS_TOPIC_ARN}")
    
    try:
        subject = f"AWS Cost Optimization Report - {datetime.now().strftime('%B %d, %Y')}"
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=report
        )
        
        print("Email notification sent successfully")
        
    except Exception as e:
        print(f"Error sending SNS notification: {str(e)}")


def update_analysis_with_report(analysis_id: str, report: str) -> None:
    """
    Update DynamoDB record with the generated report
    """
    print(f"Updating DynamoDB record {analysis_id} with report")
    
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        table.update_item(
            Key={'id': analysis_id},
            UpdateExpression='SET ai_report = :report, report_generated_at = :timestamp',
            ExpressionAttributeValues={
                ':report': report,
                ':timestamp': datetime.now().isoformat()
            }
        )
        
        print("DynamoDB updated successfully")
        
    except Exception as e:
        print(f"Error updating DynamoDB: {str(e)}")


# For local testing
if __name__ == "__main__":
    print("Running local test...")
    
    # Mock event and context
    result = lambda_handler({}, {})
    print(json.dumps(result, indent=2))
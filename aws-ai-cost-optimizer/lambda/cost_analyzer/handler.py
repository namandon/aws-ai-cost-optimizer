"""
AWS Cost Analyzer Lambda Function
Collects CloudWatch metrics and analyzes AWS resource usage
"""

import json
import boto3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Initialize AWS clients
cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')

# Get environment variables
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'cost-optimizer-data')


def lambda_handler(event, context):
    """
    Main Lambda handler function
    Triggered by EventBridge on a schedule
    """
    print("Starting cost analysis...")
    
    try:
        # Step 1: Collect metrics from AWS
        metrics_data = collect_aws_metrics()
        
        # Step 2: Analyze the data
        analysis_results = analyze_metrics(metrics_data)
        
        # Step 3: Store results in DynamoDB
        store_results(analysis_results)
        
        # Step 4: Return success
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Cost analysis completed successfully',
                'timestamp': datetime.now().isoformat(),
                'resources_analyzed': len(metrics_data),
                'recommendations': len(analysis_results.get('recommendations', []))
            })
        }
        
    except Exception as e:
        print(f"Error during cost analysis: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


def collect_aws_metrics() -> Dict[str, Any]:
    """
    Collect metrics from various AWS services
    Uses CloudWatch API (FREE - no Cost Explorer needed)
    """
    print("Collecting AWS metrics...")
    
    metrics = {
        'ec2_instances': get_ec2_metrics(),
        'ebs_volumes': get_ebs_metrics(),
        'timestamp': datetime.now().isoformat()
    }
    
    return metrics


def get_ec2_metrics() -> List[Dict[str, Any]]:
    """
    Get EC2 instance metrics (CPU utilization, network, etc.)
    """
    print("Fetching EC2 instance metrics...")
    
    instances = []
    
    try:
        # Get all running EC2 instances
        response = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                # Get CPU utilization from CloudWatch (last 7 days average)
                cpu_stats = get_cloudwatch_metric(
                    namespace='AWS/EC2',
                    metric_name='CPUUtilization',
                    dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                    days=7
                )
                
                instances.append({
                    'instance_id': instance_id,
                    'instance_type': instance_type,
                    'cpu_average': cpu_stats['average'],
                    'cpu_max': cpu_stats['max'],
                    'launch_time': instance['LaunchTime'].isoformat(),
                })
                
        print(f"Found {len(instances)} EC2 instances")
        return instances
        
    except Exception as e:
        print(f"Error getting EC2 metrics: {str(e)}")
        return []


def get_ebs_metrics() -> List[Dict[str, Any]]:
    """
    Get EBS volume metrics and identify unused volumes
    """
    print("Fetching EBS volume metrics...")
    
    volumes = []
    
    try:
        # Get all EBS volumes
        response = ec2.describe_volumes()
        
        for volume in response['Volumes']:
            volume_id = volume['VolumeId']
            size_gb = volume['Size']
            state = volume['State']
            
            # Check if volume is attached
            is_attached = len(volume.get('Attachments', [])) > 0
            
            volumes.append({
                'volume_id': volume_id,
                'size_gb': size_gb,
                'state': state,
                'is_attached': is_attached,
                'created_time': volume['CreateTime'].isoformat()
            })
            
        print(f"Found {len(volumes)} EBS volumes")
        return volumes
        
    except Exception as e:
        print(f"Error getting EBS metrics: {str(e)}")
        return []


def get_cloudwatch_metric(namespace: str, metric_name: str, 
                          dimensions: List[Dict], days: int = 7) -> Dict[str, float]:
    """
    Get CloudWatch metric statistics
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,  # 1 day
            Statistics=['Average', 'Maximum']
        )
        
        datapoints = response['Datapoints']
        
        if not datapoints:
            return {'average': 0, 'max': 0}
        
        avg = sum(d['Average'] for d in datapoints) / len(datapoints)
        max_val = max(d['Maximum'] for d in datapoints)
        
        return {'average': round(avg, 2), 'max': round(max_val, 2)}
        
    except Exception as e:
        print(f"Error getting CloudWatch metric: {str(e)}")
        return {'average': 0, 'max': 0}


def analyze_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze collected metrics and generate recommendations
    """
    print("Analyzing metrics...")
    
    recommendations = []
    
    # Analyze EC2 instances
    for instance in metrics['ec2_instances']:
        if instance['cpu_average'] < 15:
            recommendations.append({
                'type': 'ec2_rightsize',
                'severity': 'medium',
                'resource_id': instance['instance_id'],
                'current_type': instance['instance_type'],
                'cpu_utilization': instance['cpu_average'],
                'message': f"EC2 instance {instance['instance_id']} has low CPU utilization ({instance['cpu_average']}%). Consider downsizing.",
                'estimated_savings': 50  # Simplified calculation
            })
    
    # Analyze EBS volumes
    unattached_volumes = [v for v in metrics['ebs_volumes'] if not v['is_attached']]
    
    for volume in unattached_volumes:
        recommendations.append({
            'type': 'ebs_cleanup',
            'severity': 'low',
            'resource_id': volume['volume_id'],
            'size_gb': volume['size_gb'],
            'message': f"EBS volume {volume['volume_id']} ({volume['size_gb']} GB) is unattached and costing money.",
            'estimated_savings': volume['size_gb'] * 0.10  # $0.10/GB/month
        })
    
    return {
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics,
        'recommendations': recommendations,
        'total_potential_savings': sum(r['estimated_savings'] for r in recommendations)
    }


def store_results(results: Dict[str, Any]) -> None:
    """
    Store analysis results in DynamoDB
    """
    print(f"Storing results in DynamoDB table: {TABLE_NAME}")
    
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        table.put_item(
            Item={
                'id': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                'timestamp': results['timestamp'],
                'recommendations_count': len(results['recommendations']),
                'total_potential_savings': int(results['total_potential_savings']),
                'data': json.dumps(results)
            }
        )
        
        print("Results stored successfully")
        
    except Exception as e:
        print(f"Error storing results: {str(e)}")
        raise


# For local testing
if __name__ == "__main__":
    print("Running local test...")
    result = lambda_handler({}, {})
    print(json.dumps(result, indent=2))
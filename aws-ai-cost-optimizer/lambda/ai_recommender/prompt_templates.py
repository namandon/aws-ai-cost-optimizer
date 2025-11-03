"""
Prompt Templates for AI Cost Optimization Reports
Contains structured prompts for different types of analysis
"""

SYSTEM_PROMPT = """You are an expert AWS Solutions Architect specializing in cost optimization and FinOps. 
You provide clear, actionable recommendations based on infrastructure metrics.
Your reports are professional, concise, and focused on practical cost savings."""


def get_cost_analysis_prompt(metrics_data: dict) -> str:
    """
    Generate detailed cost analysis prompt
    """
    recommendations = metrics_data.get('recommendations', [])
    total_savings = metrics_data.get('total_potential_savings', 0)
    metrics = metrics_data.get('metrics', {})
    
    # Extract resource counts
    ec2_instances = metrics.get('ec2_instances', [])
    ebs_volumes = metrics.get('ebs_volumes', [])
    
    # Calculate stats
    low_cpu_instances = [i for i in ec2_instances if i.get('cpu_average', 100) < 15]
    unattached_volumes = [v for v in ebs_volumes if not v.get('is_attached', True)]
    
    prompt = f"""
# AWS Cost Optimization Analysis Request

## Infrastructure Overview
- **Total EC2 Instances**: {len(ec2_instances)}
- **Total EBS Volumes**: {len(ebs_volumes)}
- **Underutilized Instances**: {len(low_cpu_instances)} (< 15% CPU)
- **Unattached Volumes**: {len(unattached_volumes)}
- **Estimated Monthly Savings Potential**: ${total_savings:.2f}

## Detailed Recommendations
{_format_recommendations(recommendations)}

## Your Task
Create a professional AWS cost optimization report with the following structure:

### 1. Executive Summary
- Brief overview of current state (2-3 sentences)
- Total potential savings highlighted
- Urgency level (low/medium/high)

### 2. Priority Actions (Top 3)
For each action include:
- 🎯 Specific resource ID
- 💰 Estimated monthly savings
- 📊 Current utilization/state
- ✅ Recommended action
- ⚠️ Any risks or considerations

### 3. Quick Wins (Easy Implementation)
List 2-3 actions that can be done immediately with minimal risk

### 4. Long-term Optimizations
Suggest architectural improvements for sustained cost reduction

## Formatting Guidelines
- Use emojis for visual clarity
- Keep explanations concise and actionable
- Include specific resource IDs
- Provide exact savings estimates
- Use professional but friendly tone
- Format for email readability

Generate the report now.
"""
    
    return prompt


def _format_recommendations(recommendations: list) -> str:
    """
    Format recommendations for the prompt
    """
    if not recommendations:
        return "No specific recommendations at this time."
    
    formatted = []
    for idx, rec in enumerate(recommendations, 1):
        rec_type = rec.get('type', 'unknown')
        resource_id = rec.get('resource_id', 'N/A')
        message = rec.get('message', 'No details')
        savings = rec.get('estimated_savings', 0)
        
        formatted.append(f"""
**Recommendation {idx}**: {rec_type}
- Resource: {resource_id}
- Issue: {message}
- Potential Savings: ${savings:.2f}/month
""")
    
    return "\n".join(formatted)


def get_summary_prompt(metrics_data: dict) -> str:
    """
    Generate a short summary prompt (for quick reports)
    """
    total_savings = metrics_data.get('total_potential_savings', 0)
    rec_count = len(metrics_data.get('recommendations', []))
    
    return f"""
Create a 3-sentence executive summary of AWS cost optimization findings:
- {rec_count} optimization opportunities identified
- ${total_savings:.2f} in potential monthly savings
- Focus on the single most impactful action

Keep it concise and executive-friendly.
"""


def get_comparison_prompt(current_data: dict, previous_data: dict) -> str:
    """
    Generate prompt for week-over-week comparison
    """
    current_savings = current_data.get('total_potential_savings', 0)
    previous_savings = previous_data.get('total_potential_savings', 0)
    
    change = current_savings - previous_savings
    change_percent = (change / previous_savings * 100) if previous_savings > 0 else 0
    
    return f"""
# Week-over-Week Cost Analysis

## This Week
- Potential Savings: ${current_savings:.2f}
- Recommendations: {len(current_data.get('recommendations', []))}

## Last Week
- Potential Savings: ${previous_savings:.2f}
- Recommendations: {len(previous_data.get('recommendations', []))}

## Change
- Savings Delta: ${change:.2f} ({change_percent:+.1f}%)

Analyze this trend and provide:
1. What changed and why
2. Is the infrastructure becoming more or less optimized?
3. Recommended focus areas for next week

Keep it brief and actionable.
"""


# Example usage for testing
if __name__ == "__main__":
    # Test data
    test_metrics = {
        'recommendations': [
            {
                'type': 'ec2_rightsize',
                'resource_id': 'i-0abc123',
                'message': 'Low CPU utilization',
                'estimated_savings': 45
            }
        ],
        'total_potential_savings': 45,
        'metrics': {
            'ec2_instances': [
                {'instance_id': 'i-0abc123', 'cpu_average': 12}
            ],
            'ebs_volumes': []
        }
    }
    
    print("=== COST ANALYSIS PROMPT ===")
    print(get_cost_analysis_prompt(test_metrics))
    print("\n=== SUMMARY PROMPT ===")
    print(get_summary_prompt(test_metrics))
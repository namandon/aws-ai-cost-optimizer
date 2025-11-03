"""
AI Client for Cost Optimization Recommendations
Supports multiple AI providers: Groq (FREE), OpenRouter, Ollama
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional


class AIClient:
    """
    Unified AI client that works with multiple providers
    """
    
    def __init__(self):
        self.provider = os.environ.get('AI_PROVIDER', 'groq').lower()
        self.api_key = self._get_api_key()
        self.model = os.environ.get('AI_MODEL', self._get_default_model())
        self.temperature = float(os.environ.get('AI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.environ.get('AI_MAX_TOKENS', '2000'))
        
    def _get_api_key(self) -> Optional[str]:
        """Get API key based on provider"""
        if self.provider == 'groq':
            return os.environ.get('GROQ_API_KEY')
        elif self.provider == 'openrouter':
            return os.environ.get('OPENROUTER_API_KEY')
        elif self.provider == 'ollama':
            return None  # Ollama doesn't need API key
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def _get_default_model(self) -> str:
        """Get default model based on provider"""
        defaults = {
            'groq': 'llama-3.1-70b-versatile',
            'openrouter': 'anthropic/claude-3.5-sonnet',
            'ollama': 'llama3.1'
        }
        return defaults.get(self.provider, 'llama-3.1-70b-versatile')
    
    def generate_report(self, metrics_data: Dict[str, Any]) -> str:
        """
        Generate cost optimization report using AI
        """
        print(f"Generating report using {self.provider} with model {self.model}")
        
        # Build the prompt
        prompt = self._build_prompt(metrics_data)
        
        # Call appropriate provider
        if self.provider == 'groq':
            return self._call_groq(prompt)
        elif self.provider == 'openrouter':
            return self._call_openrouter(prompt)
        elif self.provider == 'ollama':
            return self._call_ollama(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _build_prompt(self, metrics_data: Dict[str, Any]) -> str:
        """
        Build the prompt for AI based on collected metrics
        """
        recommendations = metrics_data.get('recommendations', [])
        total_savings = metrics_data.get('total_potential_savings', 0)
        
        # Count resource types
        ec2_count = len(metrics_data.get('metrics', {}).get('ec2_instances', []))
        ebs_count = len(metrics_data.get('metrics', {}).get('ebs_volumes', []))
        
        prompt = f"""You are an AWS cost optimization expert. Analyze this infrastructure data and create a clear, actionable cost optimization report.

INFRASTRUCTURE SUMMARY:
- EC2 Instances: {ec2_count}
- EBS Volumes: {ebs_count}
- Total Potential Savings: ${total_savings:.2f}/month

RECOMMENDATIONS FOUND:
{json.dumps(recommendations, indent=2)}

Create a professional cost optimization report with:
1. Executive Summary (2-3 sentences)
2. Top 3 Priority Actions (with specific resource IDs and savings)
3. Quick Wins (easy to implement)
4. Long-term Optimizations

Use clear formatting with emojis for readability. Be specific and actionable.
Keep the tone professional but friendly."""

        return prompt
    
    def _call_groq(self, prompt: str) -> str:
        """
        Call Groq API (FREE - 6K requests/day)
        """
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AWS cost optimization expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Groq API: {str(e)}")
            return self._fallback_report(prompt)
    
    def _call_openrouter(self, prompt: str) -> str:
        """
        Call OpenRouter API ($0-3/month)
        """
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/aws-ai-cost-optimizer",
            "X-Title": "AWS Cost Optimizer"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AWS cost optimization expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API: {str(e)}")
            return self._fallback_report(prompt)
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API (100% FREE - self-hosted)
        """
        ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
        url = f"{ollama_host}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result['response']
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {str(e)}")
            return self._fallback_report(prompt)
    
    def _fallback_report(self, prompt: str) -> str:
        """
        Generate a basic report if AI API fails
        """
        return """
🤖 AWS COST OPTIMIZATION REPORT (Fallback Mode)

⚠️ AI service temporarily unavailable. Basic analysis provided:

📊 ANALYSIS COMPLETED
Your infrastructure has been analyzed. Check the DynamoDB table for detailed metrics.

💡 RECOMMENDATIONS
Review the recommendations stored in the database for cost savings opportunities.

🔧 NEXT STEPS
1. Check CloudWatch Logs for detailed metrics
2. Review DynamoDB entries for full analysis
3. Retry AI analysis when service is available

For detailed insights, please check your DynamoDB table.
        """


# For local testing
if __name__ == "__main__":
    # Test with sample data
    test_data = {
        'recommendations': [
            {
                'type': 'ec2_rightsize',
                'resource_id': 'i-1234567890',
                'estimated_savings': 50
            }
        ],
        'total_potential_savings': 50,
        'metrics': {
            'ec2_instances': [{'instance_id': 'i-1234567890'}],
            'ebs_volumes': []
        }
    }
    
    client = AIClient()
    report = client.generate_report(test_data)
    print(report)
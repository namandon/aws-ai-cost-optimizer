# 🤖 AI-Powered AWS Cost Optimizer

[![AWS](https://img.shields.io/badge/AWS-Free%20Tier-FF9900?logo=amazon-aws)](https://aws.amazon.com/free/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![Cost](https://img.shields.io/badge/Monthly%20Cost-$0--3-success)](/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Intelligent cloud cost monitoring powered by AI - Built entirely on AWS Free Tier**  
> Automatically analyzes AWS infrastructure and generates actionable insights using GenAI for under $3/month

---

## 🎯 **Problem Statement**

Cloud costs can spiral out of control without proper monitoring. Manual analysis is time-consuming, and traditional tools are expensive or require deep AWS expertise. 

**This project solves that by:**
- ✅ Running entirely on AWS Free Tier (minimal cost)
- ✅ Using AI to explain costs in plain English
- ✅ Automating weekly infrastructure analysis
- ✅ Providing actionable recommendations
- ✅ Demonstrating modern cloud + AI engineering skills

---

## 💰 **Cost Breakdown**

| Service | Free Tier Limit | Our Usage | Monthly Cost |
|---------|-----------------|-----------|--------------|
| **Lambda** | 1M requests + 400K GB-sec | ~8 invocations/month | **$0.00** ✅ |
| **DynamoDB** | 25 GB + 200M requests | <1 GB storage | **$0.00** ✅ |
| **EventBridge** | Unlimited schedule rules | 1 weekly rule | **$0.00** ✅ |
| **SNS** | 1,000 email notifications | ~4-8 emails/month | **$0.00** ✅ |
| **S3** | 5 GB storage + 20K GET + 2K PUT | <100 MB reports | **$0.00** ✅ |
| **CloudWatch Logs** | 5 GB ingestion + 5 GB storage | <500 MB logs | **$0.00** ✅ |
| **AI API (Optional)** | Pay-as-you-go | ~2K tokens/week | **$0-3.00** ⚠️ |
| **TOTAL** | | | **$0-3/month** 🎉 |

> **Alternative:** Use free AI options (Groq: 6K requests/day FREE, or Ollama: 100% free self-hosted) for $0 total cost!

---

## 🏗️ **Architecture**
```
┌─────────────────────────────────────────────────────────┐
│              AWS FREE TIER INFRASTRUCTURE                │
└─────────────────────────────────────────────────────────┘

 EventBridge (Weekly Trigger)
        ↓
 Lambda: Cost Analyzer
 ├─ Collects CloudWatch Metrics (FREE API)
 ├─ Analyzes EC2, EBS, S3, Lambda usage
 └─ Stores data in DynamoDB
        ↓
 Lambda: AI Recommender
 ├─ Retrieves historical data
 ├─ Calls AI API (Groq/OpenRouter/Ollama)
 └─ Generates natural language report
        ↓
 SNS → Email Notification
        ↓
 📧 Cost Optimization Report in Your Inbox
```

---

## ✨ **Features**

### **Cost Analysis**
- 📊 EC2 instance utilization (CPU, memory, network)
- 💾 EBS volume usage and idle detection
- 🗄️ S3 bucket size and access patterns
- ⚡ Lambda invocation costs
- 🔍 Orphaned resource detection (unattached volumes, old snapshots)

### **AI-Powered Insights**
- 🤖 Natural language cost reports (no technical jargon)
- 📈 Week-over-week trend analysis
- 🎯 Rightsizing recommendations (downsize over-provisioned resources)
- 💡 AWS best practice suggestions
- ⚠️ Cost anomaly detection (unexpected spikes)

### **DevOps Best Practices**
- 🚀 100% Infrastructure as Code (Terraform)
- 🔄 CI/CD pipeline with GitHub Actions
- 🧪 Automated testing
- 📊 CloudWatch monitoring and alarms
- 🔐 IAM least privilege security
- 📝 Comprehensive documentation

---

## 🚀 **Quick Start**

### **Prerequisites**
- AWS Account (free tier eligible)
- Terraform >= 1.5.0
- Python >= 3.11
- AWS CLI configured
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/aws-ai-cost-optimizer.git
cd aws-ai-cost-optimizer
```

### **2. Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Add your AI API key (optional - use free tier options)
```

### **3. Deploy Infrastructure**
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

### **4. Verify Deployment**
```bash
# Check Lambda functions
aws lambda list-functions --query 'Functions[?contains(FunctionName, `cost-optimizer`)].FunctionName'

# View logs
aws logs tail /aws/lambda/cost-analyzer-function --follow
```

---

## 📊 **Sample Output**
```
═══════════════════════════════════════════════════════════
 AWS COST OPTIMIZATION REPORT
 Week of January 27, 2025
═══════════════════════════════════════════════════════════

💰 ESTIMATED WEEKLY COST: $142.50
📊 TREND: ↑ 18% from last week

🎯 TOP 3 OPTIMIZATION OPPORTUNITIES:

1. 📉 RIGHTSIZE EC2 INSTANCE (Save $89/month)
   Instance: i-0abc1234 (t3.large)
   Avg CPU: 12% | Avg Memory: 28%
   👉 Downsize to t3.small - still meets your needs

2. 🗑️ CLEANUP UNUSED EBS VOLUMES (Save $24/month)
   Found: 3 unattached volumes (180 GB)
   Age: 45+ days unattached
   👉 Safe to delete after backup verification

3. 📦 OPTIMIZE S3 STORAGE CLASS (Save $31/month)
   Bucket: app-logs-bucket (487 GB)
   Access: <5 times in 30 days
   👉 Move to S3 Glacier or Intelligent-Tiering

💡 TOTAL POTENTIAL SAVINGS: $144/month (50.6% reduction)

Next analysis: February 3, 2025 09:00 UTC
```

---

## 🛠️ **Technology Stack**

**Cloud Services:**
- AWS Lambda (Serverless compute)
- Amazon DynamoDB (NoSQL database)
- Amazon EventBridge (Scheduling)
- Amazon SNS (Notifications)
- Amazon S3 (Storage)
- AWS CloudWatch (Metrics & Logging)

**Infrastructure:**
- Terraform (Infrastructure as Code)
- GitHub Actions (CI/CD)

**AI/ML:**
- OpenRouter API / Groq / Ollama
- LLM integration (Claude, Llama, GPT)
- Prompt engineering

**Languages & Tools:**
- Python 3.11+ (boto3, requests)
- Bash scripting
- Git version control

---

## 🎓 **What You'll Learn**

Building this project teaches:
- ✅ AWS Lambda serverless architecture
- ✅ EventBridge automation and scheduling
- ✅ DynamoDB data modeling
- ✅ CloudWatch Metrics API integration
- ✅ Infrastructure as Code with Terraform
- ✅ GenAI/LLM API integration
- ✅ Cost-conscious cloud architecture
- ✅ CI/CD pipeline development
- ✅ Python boto3 SDK
- ✅ IAM security best practices

---

## 🔒 **Security Features**

- ✅ IAM roles with least privilege
- ✅ No hardcoded credentials
- ✅ Encrypted DynamoDB tables
- ✅ Encrypted S3 buckets
- ✅ VPC not required (serverless)
- ✅ CloudWatch alarms for errors
- ✅ Automated log rotation

---

## 🧹 **Cleanup**

To avoid any charges, destroy all resources when done:
```bash
cd terraform
terraform destroy -auto-approve
```

---

## 📚 **Documentation**

- [Setup Guide](docs/setup-guide.md) - Detailed installation steps
- [Free Tier Optimization](docs/free-tier-optimization.md) - How to minimize costs
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

---

## 🎯 **Resume Bullet Points**

Use these on your resume/LinkedIn:
```
- Architected serverless cost optimization platform using AWS Lambda, 
  DynamoDB, and GenAI, enabling 40-50% infrastructure cost reduction

- Implemented AI-powered recommendation engine with LLMs, generating 
  natural language insights from CloudWatch metrics and usage patterns

- Designed 100% free-tier solution demonstrating cost-conscious 
  engineering and cloud financial management expertise

- Automated infrastructure deployment with Terraform and CI/CD pipeline, 
  reducing deployment time from hours to 3 minutes
```

---

## 🤝 **Contributing**

Contributions welcome! Ideas for improvement:
- Multi-cloud support (Azure, GCP)
- Slack/Teams integration
- QuickSight dashboard
- ML-based anomaly detection
- Mobile app notifications

---

## 📝 **License**

MIT License - Free to use for your portfolio and projects!

---

## 🙋 **Contact**

- 📧 Email: Adeoyeologunmeta@gmail.com
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/adeoyeologunmeta-724b57218)
- 🐙 GitHub: [@yourusername](https://github.com/credchampion)

---

**⭐ If this project helps your job search, please star the repo!**

**Built with ❤️ to showcase Cloud + AI engineering skills**
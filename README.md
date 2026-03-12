# AWS Serverless Projects

Collection of AWS infrastructure and automation projects demonstrating DevOps practices.

## Projects

### 1. Serverless REST API
**Technologies:** AWS Lambda, API Gateway, RDS (MySQL), VPC, Python

Production-ready REST API with three endpoints:
- `GET /health` - Database health monitoring
- `GET /records` - Retrieve all records  
- `POST /records` - Create new records

**Key features:**
- Serverless architecture (Lambda + API Gateway)
- Secure database access via VPC and Security Groups
- CORS-enabled for browser access
- Error handling and logging via CloudWatch

### 2. Automated Database Health Monitor
**Technologies:** AWS Lambda, EventBridge, CloudWatch, Python

Automated monitoring system that runs every 5 minutes:
- Queries database metrics (record count, size, status)
- Logs health data to CloudWatch
- Demonstrates scheduled automation and operational monitoring

### 3. Event-Driven File Processor
**Technologies:** AWS Lambda, S3, Python, IAM

S3-triggered Lambda function for automated file processing:
- Analyzes uploaded text files (word count, line count, character count)
- Generates analysis reports
- Stores results back in S3
- Event-driven architecture with zero manual intervention

## Skills Demonstrated
- AWS infrastructure (Lambda, EC2, RDS, S3, API Gateway, EventBridge, VPC, IAM)
- Python scripting and automation
- Bash/Shell scripting (Linux administration)
- Infrastructure security (Security Groups, VPC design)
- Serverless architecture patterns
- Database management (MySQL/RDS)
- Monitoring and observability (CloudWatch)

## Technical Challenges Solved
- VPC networking and security group configuration
- CORS implementation for web API access
- MySQL authentication methods (caching_sha2_password vs mysql_native_password)
- Lambda packaging and deployment
- Event-driven trigger configuration

---

*Built independently while learning AWS and DevOps practices.*

# Boto3 AWS Resource Management

This project uses [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to automate the creation of AWS infrastructure using Python.

Boto3 is the official AWS SDK (Software Development Kit) for Python.
It lets Python developers interact with AWS services like EC2, S3, RDS, VPC, Lambda, IAM, and many more — all through code instead of clicking through the AWS Console.

---

## 🚀 Features

- ✅ VPC with public and private subnets
- ✅ Internet Gateway and route tables
- ✅ EC2 instance using the latest Amazon Linux 2 AMI
- ✅ Security group with dynamic IP detection
- ✅ RDS instance creation with automatic AZ fallback

---

## 📁 Folder Structure

Boto/
├── Boto_create_vpc.py # Sets up VPC, subnets, EC2, and networking
├── smart_rds_launch.py # (Optional) Attempts resilient RDS creation
└── README.md


---

## ⚙️ Prerequisites

- Python 3.x installed
- Install dependencies:

```bash
pip install boto3 requests
```

    AWS credentials configured via:

        ~/.aws/credentials, or

        aws configure, or

        IAM Role (if running from EC2, Lambda, etc.)

🧪 How to Run
1. (Optional) Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate

2. Install requirements

pip install boto3 requests

3. Run the main infrastructure script

python Boto_create_vpc.py

4. (Optional) Launch the dynamic RDS setup

python smart_rds_launch.py

    The smart_rds_launch.py script intelligently tests AZ combinations to avoid common RDS launch failures due to capacity issues.

🔒 Security Best Practices

    ❌ Do not hardcode AWS credentials in your scripts

    ✅ Use ~/.aws/credentials, environment variables, or IAM roles

    🚫 Avoid 0.0.0.0/0 in security groups unless strictly necessary

    🔁 Rotate access keys periodically

    🔐 Consider .env files (not committed to Git) for secrets

✅ Example .gitignore

__pycache__/
*.pyc
venv/
.env
*.log

📄 License

This project is private and intended for internal or educational use. Contact the author for reuse or licensing inquiries.


---

Would you like me to create a `requirements.txt` or GitHub Actions CI workflow as well?


# AWS Automation Project with Terraform, Jinja2, and Boto3

This project is an AWS automation tool built with Python.
It dynamically generates a Terraform configuration using **Jinja2**, deploys infrastructure using **Terraform**, and validates the deployed resources using **Boto3**.

---

## 🚀 Features

* Takes user input for AMI, instance type, and ALB name
* Generates Terraform code using Jinja2 templating
* Deploys EC2 + Application Load Balancer (ALB) on AWS
* Validates deployment and saves output as JSON

---

## 🛠️ Requirements

* Python 3.8+
* Terraform installed and added to PATH
* AWS credentials configured (`aws configure` or env vars)
* Python packages:

  ```bash
  pip install -r requirements.txt
  ```

---

## ▶️ How to Run

1. Clone this repo:

   ```bash
   git clone https://github.com/roy3drucker/aws_automation_project.git
   cd aws-automation-project
   ```

2. Run the script:

   ```bash
   python3 main.py
   ```

3. Enter the required input when prompted:

   * AMI type (Ubuntu / Amazon Linux)
   * Instance type (t3.small / t3.medium)
   * Region (only `us-east-2` is accepted)
   * ALB name

4. Script will:

   * Render Terraform config to `generated/main.tf`
   * Run `terraform init`, `plan`, `apply`
   * Use Boto3 to validate that resources exist
   * Save results to `aws_validation.json`

---

## 📁 Project Structure

```
.
├── main.py                      # Main script
├── aws_validator.py            # Resource validation logic using Boto3
├── aws_validation.json         # Output JSON file after validation
├── requirements.txt            # Python dependencies
├── templates/
│   └── main.tf.j2              # Jinja2 template for Terraform
├── scripts/
│   ├── user_input.py           # Collects user input
│   ├── render_template.py      # Renders Jinja2 templates
│   └── terraform_runner.py     # Executes Terraform commands
├── generated/
│   ├── main.tf                 # Rendered Terraform config
│   ├── terraform.tfstate       # Terraform state file
│   ├── terraform.tfstate.backup
│   └── tfplan                  # Terraform plan output
└── README.md
```

---

## ✅ Example Output

```json
{
  "instance_id": "i-0abc12345def67890",
  "instance_state": "running",
  "public_ip": "3.91.202.100",
  "load_balancer_dns": "my-alb-123456.elb.amazonaws.com"
}
```

---

## 📸 Screenshots

> Add screenshots here showing successful deployment (Terraform output, AWS console, etc)

* ![Terraform Apply Success](images/terraform-success.png)
* ![EC2 on AWS](images/ec2-instance.png)
* ![ALB on AWS](images/alb-success.png)

---

## ⚠️ Notes

* Script automatically rejects invalid regions and defaults to `us-east-2`
* All errors are handled with `try-except` blocks
* Resources can be destroyed using:

  ```bash
  terraform destroy
  ```
* `.terraform/`, `__pycache__/`, `.tfstate`, `.backup`, and `tfplan` should be excluded using `.gitignore`

---

## 📌 Author

Made by Roy Drucker

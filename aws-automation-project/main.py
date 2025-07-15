import logging
from scripts.user_input import get_user_input
from scripts.render_template import render_template
from scripts.terraform_runner import run_terraform

class AWSAutomationProject:
    """
    Main class to handle the AWS Automation Project flow:
    - Collect user input
    - Render Terraform configuration using Jinja2
    - Run Terraform (init, plan, apply)
    """

    def __init__(self):
        self.config = None
        self.terraform_output = None
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def collect_user_input(self):
        """Collect and validate user input for AWS resources."""
        self.config = get_user_input()

    def generate_terraform(self):
        """Render Terraform configuration file using Jinja2 template."""
        render_template(self.config)

    def apply_terraform(self):
        """Run Terraform (init, plan, apply) and capture outputs."""
        self.terraform_output = run_terraform()

    def run(self):
        """Run the main project workflow with error handling."""
        try:
            self.collect_user_input()
            logging.info("Configuration collected successfully:")
            logging.info(f"AMI: {self.config.ami}")
            logging.info(f"Instance Type: {self.config.instance_type}")
            logging.info(f"Region: {self.config.region}")
            logging.info(f"Availability Zone: {self.config.availability_zone}")
            logging.info(f"Load Balancer Name: {self.config.lb_name}")

            self.generate_terraform()
            logging.info("Terraform configuration generated successfully")

            self.apply_terraform()
            logging.info("Terraform Output:")
            logging.info(self.terraform_output)

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            raise

if __name__ == "__main__":
    app = AWSAutomationProject()
    app.run()

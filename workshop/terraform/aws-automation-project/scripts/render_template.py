"""
render_template.py

Renders the main Terraform configuration file using a Jinja2 template,
based on user-provided AWSConfig.
"""

import os
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def render_template(config):
    """
    Render the Terraform template with the provided configuration.

    Args:
        config (AWSConfig): Configuration object with AWS settings
    """
    try:
        # Get absolute paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        templates_dir = os.path.join(base_dir, "Templates")
        generated_dir = os.path.join(base_dir, "generated")

        # Ensure the generated directory exists
        os.makedirs(generated_dir, exist_ok=True)

        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))

        # Load and render template
        try:
            template = env.get_template("main.tf.j2")
        except TemplateNotFound:
            logging.error("Template main.tf.j2 not found in Templates directory!")
            raise

        rendered_tf = template.render(
            region=config.region,
            ami=config.ami.value,
            instance_type=config.instance_type.value,
            availability_zone=config.availability_zone,
            load_balancer_name=config.lb_name,
            environment="dev",  # Default values for new template parameters
            owner="DevOps-Team"
        )

        # Save rendered template
        output_path = os.path.join(generated_dir, "main.tf")
        with open(output_path, "w") as f:
            f.write(rendered_tf)

        logging.info(f"Successfully generated Terraform configuration at {output_path}")

    except Exception as e:
        logging.error(f"Failed to render template: {str(e)}")
        raise

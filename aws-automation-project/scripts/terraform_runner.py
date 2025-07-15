"""
terraform_runner.py

Handles all Terraform lifecycle commands for deployment,
including init, plan, apply, output, and destroy,
with robust error handling and live progress display.
"""

import os
import shutil
import logging
import subprocess

def check_terraform_installed():
    """Check if Terraform is installed and accessible."""
    if not shutil.which("terraform"):
        raise RuntimeError(
            "Terraform is not installed or not in PATH. "
            "Please install Terraform and try again."
        )

def run_command(command, working_dir, timeout=300):
    """
    Run a command in a given working directory and return its output.
    Shows real-time progress with visual indicators.
    """
    try:
        process = subprocess.Popen(
            command,
            cwd=working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        logging.info(f"Running command: {' '.join(command)}")
        print("Progress: ", end="", flush=True)

        stdout_lines = []
        stderr_lines = []
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()

            if stdout_line:
                stdout_lines.append(stdout_line)
                if "Creating..." in stdout_line or "Modifying..." in stdout_line:
                    print("🔄", end="", flush=True)
                elif "Creation complete" in stdout_line or "Modifications complete" in stdout_line:
                    print("✅", end="", flush=True)
            if stderr_line:
                stderr_lines.append(stderr_line)
                if "Error:" in stderr_line:
                    print("❌", end="", flush=True)
            if not stdout_line and not stderr_line and process.poll() is not None:
                break

        logging.info("")  # New line after progress indicators

        process.wait(timeout=timeout)

        result = type('Result', (), {
            'returncode': process.returncode,
            'stdout': ''.join(stdout_lines),
            'stderr': ''.join(stderr_lines)
        })

        if result.stdout:
            logging.info(f"Command output:\n{result.stdout}")
        if result.stderr:
            logging.error(f"Command error:\n{result.stderr}")

        return result

    except subprocess.TimeoutExpired:
        process.kill()
        raise Exception(f"Command timed out after {timeout} seconds: {' '.join(command)}")
    except Exception as e:
        raise Exception(f"Command failed: {' '.join(command)}\nError: {str(e)}")

def run_terraform():
    """
    Run Terraform commands to deploy the infrastructure.
    Returns:
        str: The output of 'terraform output -json' as a JSON string.
    Raises:
        Exception: If any Terraform command fails.
    """
    check_terraform_installed()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generated_dir = os.path.join(base_dir, "generated")

    logging.info(f"Working directory: {generated_dir}")

    try:
        logging.info("\nInitializing Terraform...")
        init_result = run_command(["terraform", "init"], generated_dir, timeout=60)
        if init_result.returncode != 0:
            raise Exception("Terraform init failed")

        logging.info("\nPlanning Terraform changes...")
        plan_result = run_command(["terraform", "plan", "-out=tfplan"], generated_dir, timeout=120)
        if plan_result.returncode != 0:
            raise Exception("Terraform plan failed")

        if "No changes" not in plan_result.stdout:
            logging.info("\nShowing detailed plan...")
            show_result = run_command(["terraform", "show", "tfplan"], generated_dir, timeout=30)
            if show_result.returncode != 0:
                raise Exception("Failed to show plan")

        logging.info("\nApplying Terraform changes...")
        logging.info("This might take a few minutes as resources are being created...")
        apply_result = run_command(["terraform", "apply", "-auto-approve"], generated_dir, timeout=600)
        if apply_result.returncode != 0:
            raise Exception("Terraform apply failed")

        logging.info("\n✨ Deployment completed successfully! ✨")

        output_result = run_command(["terraform", "output", "-json"], generated_dir, timeout=30)
        return output_result.stdout if output_result.returncode == 0 else "{}"

    except Exception as e:
        logging.error(f"Terraform operation failed: {str(e)}")
        raise

def destroy_infrastructure():
    """
    Run Terraform destroy to remove all deployed resources.
    """
    check_terraform_installed()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generated_dir = os.path.join(base_dir, "generated")

    try:
        process = subprocess.Popen(
            ["terraform", "destroy", "-auto-approve"],
            cwd=generated_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Destroy Progress: ", end="", flush=True)
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
            elif process.poll() is not None:
                break

        process.wait()
        if process.returncode != 0:
            logging.error("Terraform destroy failed.")
            raise Exception("Terraform destroy failed.")
        logging.info("All resources destroyed successfully.")
    except Exception as e:
        logging.error(f"Failed to destroy infrastructure: {str(e)}")
        raise

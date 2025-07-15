"""
aws_config.py

Defines AWSConfig dataclass for EC2/ALB deployment,
input validation, and user prompt logic for the automation project.
"""

import re
from dataclasses import dataclass
from enum import Enum

DEFAULT_REGION = "us-east-2"

class InstanceType(str, Enum):
    SMALL = "t3.small"
    MEDIUM = "t3.medium"

class AMIType(str, Enum):
    UBUNTU = "ami-0c995fbcf99222492"
    AMAZON_LINUX = "ami-0915e09cc7ceee3ab"

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

@dataclass
class AWSConfig:
    """Configuration class for AWS resources."""
    ami: AMIType
    instance_type: InstanceType
    region: str
    availability_zone: str
    lb_name: str

    @staticmethod
    def _validate_lb_name(name: str) -> bool:
        """
        Validate load balancer name according to AWS rules.
        """
        if not name or len(name) > 32:
            return False
        if name.startswith('-') or name.endswith('-'):
            return False
        if not re.match('^[a-zA-Z0-9-]+$', name):
            return False
        aws_regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]
        if name.lower() in aws_regions:
            print("Load balancer name cannot be an AWS region name")
            return False
        return True

    @staticmethod
    def _get_validated_input(prompt: str, options: dict, default: str):
        """Get and validate user input against a set of options."""
        while True:
            print(f"\n{prompt}")
            for key, (name, _) in options.items():
                print(f"{key} - {name}")
            choice = input(f"Enter your choice [{'/'.join(options.keys())}]: ").strip()
            if choice in options:
                return options[choice]
            print(f"Invalid choice. Using default: {options[default][0]}")
            return options[default]

    @classmethod
    def from_user_input(cls) -> "AWSConfig":
        """
        Prompt user for all required AWS configuration values.
        Returns:
            AWSConfig: validated config
        """
        print("=== AWS EC2 Deployment Configurator ===")

        # AMI Selection with validation
        ami_map = {
            "1": ("Ubuntu 24.04 LTS", AMIType.UBUNTU),
            "2": ("Amazon Linux 2023", AMIType.AMAZON_LINUX)
        }
        _, ami = cls._get_validated_input(
            "Choose AMI:",
            ami_map,
            default="1"
        )

        # Instance Type Selection with validation
        instance_map = {
            "1": ("t3.small", InstanceType.SMALL),
            "2": ("t3.medium", InstanceType.MEDIUM)
        }
        _, instance_type = cls._get_validated_input(
            "Choose Instance Type:",
            instance_map,
            default="1"
        )

        # Region Input (only us-east-2 supported for now)
        region = DEFAULT_REGION
        print(f"\nUsing region: {region} (only supported region)")

        # Availability Zone
        availability_zone = f"{region}a"
        print(f"Using availability zone: {availability_zone}")

        # Load Balancer Name with improved validation
        while True:
            lb_name = input("\nEnter a name for the Load Balancer: ").strip()
            if cls._validate_lb_name(lb_name):
                break
            print("Load balancer name must:")
            print("- Be between 1 and 32 characters")
            print("- Contain only letters, numbers, and hyphens")
            print("- Not begin or end with a hyphen")

        return cls(
            ami=ami,
            instance_type=instance_type,
            region=region,
            availability_zone=availability_zone,
            lb_name=lb_name
        )

import subprocess

def is_docker_installed():
    try:
        # Run the command `docker --version` to check Docker installation
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, check=True)
        # Check the output to confirm that Docker is available
        if "Docker version" in result.stdout:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # If the command fails (exit code != 0), Docker is not available
        return False
    except FileNotFoundError:
        # If the `docker` executable is not found, Docker is not installed
        return False

# Example usage
if is_docker_installed():
    print("Docker is installed.")
else:
    print("Docker is not installed.")
    
    
import subprocess

def is_aws_cli_installed():
    try:
        # Check AWS CLI installation by running `aws --version`
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True, check=True)
        if "aws-cli" in result.stdout or result.stderr:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def is_aws_connected():
    try:
        # Verify if AWS CLI is connected by calling `sts get-caller-identity`
        result = subprocess.run(
            ['aws', 'sts', 'get-caller-identity'], capture_output=True, text=True, check=True
        )
        # If the command runs successfully, the user is authenticated
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # Non-zero exit code means the credentials aren't configured or valid
        return False
    except FileNotFoundError:
        # AWS CLI is not installed
        return False

# Example usage
if is_aws_cli_installed():
    print("AWS CLI is installed.")
    if is_aws_connected():
        print("AWS CLI is connected to an AWS account.")
    else:
        print("AWS CLI is not connected to an AWS account.")
else:
    print("AWS CLI is not installed.")
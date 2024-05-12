import subprocess
from rich.progress import Progress

# Replace this with the HTTPS URL of your Git repository
repo_url = "https://github.com/user/repo.git"

# Initialize Rich progress bar
with Progress() as progress:
    task1 = progress.add_task("[green]Fetching branches...", total=100)

    try:
        # Use subprocess to execute the git command
        process = subprocess.Popen(['git', 'ls-remote', '--heads', repo_url],
                                   stdout=subprocess.PIPE, text=True)

        # Create a buffer to store the output
        output_lines = []
        
        # Read the output line by line
        while True:
            line = process.stdout.readline()
            if not line:
                break
            output_lines.append(line)
            # Update progress bar
            progress.update(task1, advance=10)

        # Wait for process to complete and get the final status
        process.wait()
        
        # Parse the output to extract branch names
        branches = [line.split('\t')[1].replace('refs/heads/', '') for line in output_lines]

        # Complete the task
        progress.update(task1, completed=100)

        # Print the list of branches
        print("Branches:")
        for branch in branches:
            print(branch)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running git command: {e}")
        
        
import subprocess
from rich.progress import Progress

# Replace this with the HTTPS URL of your Git repository
repo_url = "https://github.com/user/repo.git"

def fetch_branches(repo_url):
    # Run git ls-remote command to fetch branches
    result = subprocess.run(['git', 'ls-remote', '--heads', repo_url], text=True, capture_output=True)
    if result.returncode == 0:
        return result.stdout.splitlines()
    else:
        raise Exception("Failed to fetch branches")

# Use rich to create and manage a progress bar
with Progress() as progress:
    task = progress.add_task("[cyan]Fetching branches...", total=100)
    
    # Fetch branches
    branches_data = fetch_branches(repo_url)
    
    # Parse the output to extract branch names
    branches = []
    for i, line in enumerate(branches_data):
        parts = line.split('\t')
        branch_name = parts[1].replace('refs/heads/', '')
        branches.append(branch_name)
        
        # Update progress based on the number of lines
        progress.update(task, advance=100 / len(branches_data))

    # Complete the progress bar
    progress.update(task, completed=100)

    # Print the list of branches
    print("Branches:")
    for branch in branches:
        print(branch)
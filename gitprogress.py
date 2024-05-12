import os
import click
from git import Repo
from git import RemoteProgress

class CloneProgress(RemoteProgress):
    def __init__(self, max_steps):
        super().__init__()
        self.step = 0
        self.max_steps = max_steps

    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count:
            self.step = (cur_count / max_count) * self.max_steps
            self.progress.update(self.step)

@click.command()
@click.argument('repository_url')
@click.argument('file_path')
def fetch_file(repository_url, file_path):
    local_path = "/tmp/repo"
    
    # Prepare to delete any existing directory to clean start
    if os.path.exists(local_path):
        import shutil
        shutil.rmtree(local_path)

    with click.progressbar(length=100, label='Cloning repository') as bar:
        progress = CloneProgress(max_steps=100)
        progress.progress = bar
        repo = Repo.clone_from(repository_url, local_path, progress=progress)
    
    # Attempt to open and print the file from the cloned repository
    try:
        with open(os.path.join(local_path, file_path), 'r') as file:
            click.echo(f"\nContents of {file_path}:")
            click.echo(file.read())
    except FileNotFoundError:
        click.echo(f"File {file_path} not found in the repository.")

if __name__ == '__main__':
    fetch_file()
    
##################
import os
from git import Repo
from git import RemoteProgress
from rich.progress import Progress

class CloneProgress(RemoteProgress):
    def __init__(self, progress):
        super().__init__()
        self.progress = progress
        self.task_id = self.progress.add_task("[cyan]Cloning...", total=100)

    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count:
            self.progress.update(self.task_id, advance=(cur_count / max_count * 100))

def fetch_file(repository_url, file_path):
    local_path = "/tmp/repo"
    
    # Clean up the local directory if it exists
    if os.path.exists(local_path):
        import shutil
        shutil.rmtree(local_path)

    # Using Rich's Progress context manager to handle the progress display
    with Progress() as progress:
        git_progress = CloneProgress(progress)
        repo = Repo.clone_from(repository_url, local_path, progress=git_progress)

    # Try to read the file from the cloned repository
    try:
        with open(os.path.join(local_path, file_path), 'r') as file:
            content = file.read()
            print(f"\nContents of {file_path}:")
            print(content)
    except FileNotFoundError:
        print(f"File {file_path} not found in the repository.")

# Example usage:
if __name__ == '__main__':
    repository_url = input("Enter the repository URL: ")
    file_path = input("Enter the file path within the repository: ")
    fetch_file(repository_url, file_path)

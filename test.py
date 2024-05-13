import click
from InquirerPy import inquirer
import time

def process_with_click_progress_bar(total_items: int):
    """Simulates processing with a progress bar."""
    with click.progressbar(range(total_items), label="Processing items") as items:
        for _ in items:
            time.sleep(0.5)  # Simulate work being done

@click.command()
def select_and_process():
    """Select an option and display a progress bar for processing."""
    # Prompt user to choose an option
    selected = inquirer.select(
        message="Choose an option to process:",
        choices=["Option A", "Option B", "Option C", "Option D"]
    ).execute()

    click.echo(f"You selected: {selected}")
    click.echo("Starting processing...")

    # Start processing with progress bar
    total_items = 10
    process_with_click_progress_bar(total_items)

if __name__ == "__main__":
    select_and_process()
    
    
# editot

import click
from InquirerPy import prompt
from InquirerPy.validator import PathValidator
from rich.console import Console

console = Console()

@click.command()
@click.option('--edit', is_flag=True, help="Enable editing mode.")
def configure(edit):
    if edit:
        questions = [
            {
                "type": "input",
                "name": "username",
                "message": "Enter your username:",
            },
            {
                "type": "password",
                "name": "password",
                "message": "Enter your password:",
            },
            {
                "type": "filepath",
                "name": "config_path",
                "message": "Select a config file:",
                "validate": PathValidator(is_file=True),
                "only_files": True,
            }
        ]
        responses = prompt(questions)
        console.print("Configuration updated with:", responses, style="bold green")
    else:
        console.print("Run this command with --edit to modify configurations.", style="bold red")

if __name__ == '__main__':
    configure()
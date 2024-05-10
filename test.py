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
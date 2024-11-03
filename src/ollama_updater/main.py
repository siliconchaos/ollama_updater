#!/usr/bin/env python3

"""
Ollama Model Updater
"""

import asyncio
import logging
import subprocess

# from datetime import datetime
import sys
from enum import Enum
from typing import List

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

# Initalize rich console
console = Console()
app = typer.Typer(help="Ollama Model Updater")


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def setup_logging(log_level: str) -> None:
    """Configure logging with rich handler."""
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def check_dependencies() -> bool:
    """Check if ollama is installed and accessible."""
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        console.print("[red]Error:[/red] Ollama is not installed or not accessible.")
        return False


async def get_installed_models() -> List[str]:
    """Get list of installed Ollama models."""
    try:
        process = await asyncio.create_subprocess_exec(
            "ollama",
            "list",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await process.communicate()

        # Skip header line and empty lines
        models = [
            line.split()[0] for line in stdout.decode().splitlines()[1:] if line.strip()
        ]
        # console.print(f"models: {models}")
        return models
    except Exception as e:
        console.print(f"[red]Error getting model list:[/red] {str(e)}")
        return []


async def update_model(model: str) -> None:
    """Update a single Ollama model."""
    try:
        process = await asyncio.create_subprocess_exec(
            "ollama",
            "pull",
            model,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        success = process.returncode == 0
        output = stdout.decode() if success else stderr.decode()
        return success, output
    except Exception as e:
        return False, str(e)


async def update_all_models(models: List[str]) -> None:
    """Update all Ollama models."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        overall_task = progress.add_task("[cyan]Updating models...", total=len(models))

        for model in models:
            task_id = progress.add_task(f"[yellow]Pulling {model}...", total=1)

            success, output = await update_model(model)
            # ic(success, output)
            if success:
                progress.update(
                    task_id, completed=1, description=f"[green]Updated {model}"
                )
            else:
                progress.update(
                    task_id, completed=1, description=f"[red]Failed to update {model}"
                )
                console.print(
                    Panel(output, title=f"Error updating {model}", border_style="red")
                )

            progress.update(overall_task, advance=1)


@app.command()
def main(
    log_level: LogLevel = typer.Option(
        LogLevel.INFO, "--log-level", "-l", help="Set the logging level"
    ),
) -> None:
    """update all installed Ollama models."""
    setup_logging(log_level.value)

    console.print(Panel.fit("[cyan]Ollama Model Updater[/cyan]", border_style="blue"))

    if not check_dependencies():
        sys.exit(1)

    try:
        models = asyncio.run(get_installed_models())
        if not models:
            console.print("[yellow]No models found to update.[/yellow]")
            sys.exit(0)

        console.print(f"[green]Found {len(models)} models to update:[/green]")
        asyncio.run(update_all_models(models))

    except KeyboardInterrupt:
        console.print("\n[yellow]Update cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error updating models:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()

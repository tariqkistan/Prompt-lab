import json
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from promptlab.models import Rubric
from promptlab.scorer import score

load_dotenv()  # loads .env file

app = typer.Typer(help='Score text against a rubric using LLMs')
console = Console()


@app.command()
def main(
    text: str | None = typer.Option(
        None, '--text', '-t', help='Text to score directly'
    ),
    file: Path | None = typer.Option(
        None, '--file', '-f', help='Path to text file to score'
    ),
    rubric_file: Path = typer.Option(
        ..., '--rubric', '-r', help='Path to rubric JSON file'
    ),
    mode: str = typer.Option(
        'zero-shot', '--mode', '-m',
        help='Prompting mode: zero-shot, few-shot, or cot'
    ),
):
    """Score text against a rubric using an LLM."""
    # Get input text
    if file:
        input_text = file.read_text()
    elif text:
        input_text = text
    else:
        console.print('[red]Error: provide --text or --file[/red]')
        raise typer.Exit(1)

    # Load rubric
    rubric_data = json.loads(rubric_file.read_text())
    rubric = Rubric(**rubric_data)

    console.print(f'[bold]Scoring with mode:[/bold] {mode}')
    console.print(f'[bold]Rubric:[/bold] {rubric.name}')

    # Score
    result, tokens = score(input_text, rubric, mode)

    # Display result
    colour = 'green' if result.score >= 0.7 else 'red'
    console.print(
        Panel(
            f'[bold]Score:[/bold] [{colour}]{result.score}[/{colour}]\n'
            f'[bold]Confidence:[/bold] {result.confidence}\n'
            f'[bold]Rationale:[/bold] {result.rationale}\n'
            f'[dim]Tokens used: {tokens}[/dim]',
            title='Result',
        )
    )
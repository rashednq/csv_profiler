"""Command-line interface for CSV Profiler."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from .csv_io import read_csv_file
from .profiling import build_report, to_profile
from .render import generate_json_report, generate_markdown_report

app = typer.Typer(help="CSV Profiler - Analyze and profile CSV files")


@app.command()
def profile(
    csv_file: Path = typer.Argument(..., help="Path to the CSV file to profile", exists=True, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o", help="Output directory for reports"),
    format: str = typer.Option("json", "--format", "-f", help="Output format: json, md, or both"),
) -> None:
    """Profile a CSV file and generate statistics."""
    rows = read_csv_file(csv_file)

    report = build_report(rows)
    result = to_profile(report)

    fmt = format.lower()
    if fmt not in ("json", "md", "markdown", "both"):
        raise typer.BadParameter("format must be one of: json, md, both")

    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    if fmt in ("json", "both"):
        json_report = generate_json_report(result)
        if out_dir:
            path = out_dir / f"{csv_file.stem}_profile.json"
            path.write_text(json_report, encoding="utf-8")
            typer.echo(f"JSON report saved to: {path}")
        else:
            typer.echo(json_report)

    # Markdown
    if fmt in ("md", "markdown", "both"):
        md_report = generate_markdown_report(result)
        if out_dir:
            path = out_dir / f"{csv_file.stem}_profile.md"
            path.write_text(md_report, encoding="utf-8")
            typer.echo(f"Markdown report saved to: {path}")
        else:
            typer.echo(md_report)

    if out_dir:
        typer.echo(f"\nProfiled {result['n_rows']} rows, {result['n_cols']} columns")


@app.command()
def info(
    csv_file: Path = typer.Argument(..., help="Path to the CSV file", exists=True, readable=True),
) -> None:
    """Show basic info about a CSV file without full profiling."""
    rows = read_csv_file(csv_file)

    if not rows:
        typer.echo("Empty CSV file")
        raise typer.Exit(code=1)

    columns = list(rows[0].keys())
    typer.echo(f"File: {csv_file}")
    typer.echo(f"Rows: {len(rows)}")
    typer.echo(f"Columns: {len(columns)}")
    typer.echo(f"Column names: {', '.join(columns)}")


@app.command()
def web(
    port: int = typer.Option(8501, "--port", "-p", help="Port for Streamlit server"),
) -> None:
    """Launch the Streamlit web interface."""
    app_path = Path(__file__).parent / "app.py"
    typer.echo("Starting Streamlit app...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port", str(port)], check=True)


if __name__ == "__main__":
    app()
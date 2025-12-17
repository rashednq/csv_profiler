"""
Command-line interface for CSV Profiler.
"""

from pathlib import Path
import subprocess
import typer

from csv_profiler.csv_io import read_csv_file
from csv_profiler.profiler import build_report, to_profile
from csv_profiler.render import (
    generate_json_report,
    generate_markdown_report,
)

app = typer.Typer(help="CSV Profiler - Analyze and profile CSV files")


@app.command()
def profile(
    csv_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to CSV file",
    ),
    out_dir: Path = typer.Option(
        Path("outputs"),
        "--out-dir",
        "-o",
        help="Output directory",
    ),
    format: str = typer.Option(
        "both",
        "--format",
        "-f",
        help="json | md | both",
    ),
):
    """Profile a CSV file and generate reports."""
    rows = read_csv_file(csv_path)

    report = build_report(rows)
    profile_data = to_profile(report)

    out_dir.mkdir(parents=True, exist_ok=True)
    fmt = format.lower()

    if fmt not in ("json", "md", "both"):
        raise typer.BadParameter("format must be: json, md, or both")

    if fmt in ("json", "both"):
        json_path = out_dir / "report.json"
        json_path.write_text(
            generate_json_report(profile_data),
            encoding="utf-8",
        )
        typer.echo(f"Saved: {json_path}")

    if fmt in ("md", "both"):
        md_path = out_dir / "report.md"
        md_path.write_text(
            generate_markdown_report(profile_data),
            encoding="utf-8",
        )
        typer.echo(f"Saved: {md_path}")

    typer.echo(
        f"\nProfiled {profile_data['n_rows']} rows, "
        f"{profile_data['n_cols']} columns"
    )


@app.command()
def info(
    csv_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to CSV file",
    ),
):
    """Show basic information about a CSV file."""
    rows = read_csv_file(csv_path)

    if not rows:
        typer.echo("Empty CSV")
        raise typer.Exit(code=1)

    columns = list(rows[0].keys())
    typer.echo(f"Rows: {len(rows)}")
    typer.echo(f"Columns: {len(columns)}")
    typer.echo(f"Column names: {', '.join(columns)}")


@app.command()
def web(
    port: int = typer.Option(8501, "--port", "-p"),
):
    """Launch Streamlit web app."""
    app_path = Path(__file__).parent / "app.py"
    typer.echo("Starting Streamlit app...")
    subprocess.run(
        [
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(port),
        ],
        check=True,
    )


if __name__ == "__main__":
    app()
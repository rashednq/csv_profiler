from pathlib import Path
from typing import Optional

import typer

from csv_profiler.csv_io import read_csv
from csv_profiler.profiling import build_report, to_profile
from csv_profiler.render import generate_json_report, generate_markdown_report

app = typer.Typer(help="CSV Profiler CLI")


@app.command()
def profile(
    csv_path: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", "-o"),
    format: str = typer.Option("both", "--format", "-f"),
    output_name: Optional[str] = typer.Option(None, "--output-name", "-n"),
):
    rows = read_csv(csv_path)
    report = build_report(rows)
    profile_data = to_profile(report)

    out_dir.mkdir(parents=True, exist_ok=True)

    base = output_name or csv_path.stem
    fmt = format.lower().strip()

    if fmt not in ("json", "md", "markdown", "both"):
        raise typer.BadParameter("format must be one of: json, md, markdown, both")

    if fmt in ("json", "both"):
        json_path = out_dir / f"{base}.json"
        json_path.write_text(generate_json_report(profile_data), encoding="utf-8")
        typer.echo(f"Saved: {json_path}")

    if fmt in ("md", "markdown", "both"):
        md_path = out_dir / f"{base}.md"
        md_path.write_text(generate_markdown_report(profile_data), encoding="utf-8")
        typer.echo(f"Saved: {md_path}")


@app.command()
def info(
    csv_path: Path = typer.Argument(..., exists=True, readable=True),
):
    rows = read_csv(csv_path)
    if not rows:
        typer.echo("Empty CSV")
        raise typer.Exit(code=1)

    cols = list(rows[0].keys())
    typer.echo(f"Rows: {len(rows)}")
    typer.echo(f"Columns: {len(cols)}")


if __name__ == "__main__":
    app()

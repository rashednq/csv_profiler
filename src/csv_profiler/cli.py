from pathlib import Path
import typer

from csv_profiler.csv_io import read_csv
from csv_profiler.profiling import build_report, to_profile
from csv_profiler.render import generate_json_report, generate_markdown_report

app = typer.Typer(help="CSV Profiler CLI")


@app.command()
def profile(
    csv_path: Path = typer.Argument(..., exists=True, readable=True),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", "-o"),
):
    rows = read_csv(csv_path)
    report = build_report(rows)
    profile_data = to_profile(report)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(generate_json_report(profile_data), encoding="utf-8")
    (out_dir / "report.md").write_text(generate_markdown_report(profile_data), encoding="utf-8")

    typer.echo(f"Saved: {out_dir / 'report.json'}")
    typer.echo(f"Saved: {out_dir / 'report.md'}")


@app.command()
def info(
    csv_path: Path = typer.Argument(..., exists=True, readable=True),
):
    rows = read_csv(csv_path)
    if not rows:
        typer.echo("Empty CSV")
        raise typer.Exit()

    cols = list(rows[0].keys())
    typer.echo(f"Rows: {len(rows)}")
    typer.echo(f"Columns: {len(cols)}")


if __name__ == "__main__":
    app()
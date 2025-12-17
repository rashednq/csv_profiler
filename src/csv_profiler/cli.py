import os
import typer

from csv_io import read_csv
from profiling import build_report, to_profile
from render import print_report, save_report, save_report_md

app = typer.Typer()


@app.command()
def run(
    csv_path: str = typer.Argument(..., help="Path to CSV file"),
    out_dir: str = typer.Option("outputs", "--out"),
):
    if not os.path.isfile(csv_path):
        raise typer.BadParameter("CSV file not found")

    rows = read_csv(csv_path)
    if not rows:
        raise typer.BadParameter("Empty CSV")

    report = build_report(rows)
    profile = to_profile(report)

    os.makedirs(out_dir, exist_ok=True)

    json_path = os.path.join(out_dir, "report.json")
    md_path = os.path.join(out_dir, "report.md")

    print_report(report)
    save_report(report, json_path)
    save_report_md(profile, md_path)


if __name__ == "__main__":
    app()
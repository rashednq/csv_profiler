# CSV Profiler

CSV Profiler is a lightweight tool for analyzing CSV files and generating profiling reports.
It helps you quickly understand your data by detecting column types, missing values, and basic statistics.

The tool can be used through:
- A web interface (Streamlit)
- A command-line interface (CLI)

---

## Features

- Automatic column type detection (number / text)
- Missing values count and percentage
- Unique values count per column
- Report generation in JSON and Markdown formats
- Run directly from GitHub using `uvx`
- Simple web interface built with Streamlit

---

## Web Interface

You can launch the web interface directly from GitHub without installing anything locally.

### Run the web app

```bash
uvx git+https://github.com/rashednq/csv_profiler.git web
```

Then open your browser at:

```
http://localhost:8501
```

### From the web interface you can:
- Upload a CSV file
- Generate a profiling report
- Preview the results
- Download the report as JSON or Markdown

---

## Command Line Interface (CLI)

You can also profile CSV files directly from the terminal.

### Profile a CSV file

```bash
uvx git+https://github.com/rashednq/csv_profiler.git profile data/saudi_shopping_with_missing.csv --out-dir outputs --format both
```

### CLI Parameters

- **CSV_PATH**  
  Path to the CSV file you want to analyze

- **--out-dir**  
  Directory where the output files will be saved  
  (default: `outputs`)

- **--format**  
  Output format:
  - `json`
  - `md`
  - `both`

---

## Output

The generated files will be saved inside the specified output directory:

- `report.json`
- `report.md`

---

## Project Structure

```text
csv_profiler/
├── src/
│   └── csv_profiler/
│       ├── cli.py        # CLI implementation (Typer)
│       ├── app.py        # Streamlit web app
│       ├── profiling.py # Core profiling logic
│       ├── csv_io.py     # CSV reading utilities
│       └── render.py    # Report rendering (JSON / Markdown)
├── data/                # Sample CSV files
├── outputs/             # Generated reports
├── pyproject.toml
└── README.md
```

---

## Requirements

- Python 3.9+
- uv / uvx

> All dependencies are handled automatically when running via `uvx`.

---

## Notes

This project was built for learning purposes and focuses on clarity and simplicity.
It demonstrates how to build:
- A reusable CLI tool using **Typer**
- A lightweight web interface using **Streamlit**

import json


def print_report(report):
    print(json.dumps(report, indent=4, ensure_ascii=False))


def save_report(report, path="report.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"Saved {path}")


def display_profile_summary(profile):
    print("=" * 50)
    print("PROFILE SUMMARY")
    print("=" * 50)
    print(f"Rows: {profile['n_rows']:,}")
    print(f"Columns: {profile['n_cols']}")
    print()


def display_column_table(profile):
    print("COLUMN DETAILS")
    print("-" * 60)
    print(f"{'Column':<15} {'Type':<10} {'Missing':<15} {'Unique':<10}")
    print("-" * 60)

    for col in profile["columns"]:
        n_rows = profile["n_rows"]
        missing_pct = (col["missing"] / n_rows * 100) if n_rows else 0
        print(
            f"{col['name']:<15} "
            f"{col['type']:<10} "
            f"{col['missing']} ({missing_pct:.1f}%)     "
            f"{col['unique']}"
        )


def generate_json_report(profile):
    return json.dumps(profile, indent=2, ensure_ascii=False)


def generate_markdown_report(profile):
    lines = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- **Rows:** {profile['n_rows']:,}")
    lines.append(f"- **Columns:** {profile['n_cols']}\n")
    lines.append("## Column Summary\n")
    lines.append("| Column | Type | Missing | Unique |")
    lines.append("|--------|------|--------:|-------:|")

    for col in profile["columns"]:
        n_rows = profile["n_rows"]
        missing_pct = (col["missing"] / n_rows * 100) if n_rows else 0
        lines.append(
            f"| {col['name']} | {col['type']} | "
            f"{col['missing']} ({missing_pct:.1f}%) | {col['unique']} |"
        )

    return "\n".join(lines)


def save_report_md(profile, path="report.md"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(generate_markdown_report(profile))

    print(f"Saved {path}")
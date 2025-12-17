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
    print("-" * 72)
    print(f"{'Column':<18} {'Type':<10} {'Missing':<10} {'Missing%':<10} {'Unique':<10}")
    print("-" * 72)

    n_rows = profile["n_rows"] or 0
    cols = list(profile["columns"])
    cols.sort(key=lambda c: c.get("missing", 0), reverse=True)

    for col in cols:
        missing = col.get("missing", 0)
        unique = col.get("unique", 0)
        missing_pct = (missing / n_rows * 100) if n_rows else 0

        print(
            f"{col.get('name',''):<18} "
            f"{col.get('type',''):<10} "
            f"{missing:<10} "
            f"{missing_pct:>7.1f}%   "
            f"{unique:<10}"
        )


def generate_json_report(profile):
    return json.dumps(profile, indent=2, ensure_ascii=False)


def generate_markdown_report(profile):
    lines = []
    lines.append("# CSV Profiling Report")
    lines.append("")
    lines.append(f"- **Rows:** {profile['n_rows']:,}")
    lines.append(f"- **Columns:** {profile['n_cols']}")
    lines.append("")

    cols = list(profile["columns"])
    n_rows = profile["n_rows"]

    for c in cols:
        c["missing_pct"] = (c["missing"] / n_rows * 100) if n_rows else 0.0

    cols.sort(key=lambda c: (-c["missing_pct"], c["name"]))

    lines.append("## Column Details")
    lines.append("")
    lines.append("| Column | Type | Missing | Missing % | Unique |")
    lines.append("|:------|:-----|--------:|----------:|-------:|")

    for c in cols:
        lines.append(
            f"| {c['name']} | {c['type']} | {c['missing']:,} | {c['missing_pct']:.1f}% | {c['unique']:,} |"
        )

    return "\n".join(lines)


def save_report_md(profile, path="report.md"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(generate_markdown_report(profile))

    print(f"Saved {path}")
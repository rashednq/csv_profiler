import re

def get_column_from_name(rows, column_name):
    return [row[column_name] for row in rows]


MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan"}
def is_missing(value):
    """
    Return True if value is considered "missing".

    Args:
        value: A string value (or None)

    Returns:
        True if missing, False otherwise
    """
    if value == None:  # noqa: E711
      return True
    value = str(value).lower().strip()
    return not value or value in MISSING_VALUES


def count_missing(column_items):
        return sum(
        1
        for item in column_items
        if item is None or str(item).strip().lower() in MISSING_VALUES
    )

def get_type(column_items):
    for item in column_items:
        value = str(item).strip()
        if value == "":
            continue

        if try_float(value) is None:
            return "string"

    return "number"


def get_column_state(column_items):
    return {
        "missing": count_missing(column_items),"type": get_type(column_items)
    }
    
    
def try_float(value):
    """
    Try to convert value to float.

    Args:
        value: A string to parse

    Returns:
        float if successful, None if parsing fails
    """
    try:
        return float(value)

    except ValueError:
        return None
    
    
def numeric_stats(values):
    nums = []
    missing = 0

    for v in values:
        if is_missing(v):
            missing += 1
            continue

        n = try_float(v)
        if n is not None:
            nums.append(n)

    count = len(nums)

    return {
        "count": count,
        "missing": missing,
        "unique": len(set(nums)),
        "min": min(nums) if count else None,
        "max": max(nums) if count else None,
        "mean": sum(nums) / count if count else None,
    }


def text_stats(values, top_k=3):
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    counts = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top = [
        {"value": v, "count": c}
        for v, c in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_k]
    ]

    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }


def infer_type(values):
    """
    Infer the type of a column.

    Rules:
    - Ignore missing values
    - If ALL non-missing values parse as float -> "number"
    - Otherwise -> "text"

    Args:
        values: List of strings from a column

    Returns:
        "number" or "text"
    """
    non_missing = []
    for v in values:
        if not is_missing(v):
            non_missing.append(v)

    if not non_missing:
        return "text"

    for v in non_missing:
        if try_float(v) is None:
            return "text"

    return "number"


def slugify(text):
    """
    Convert text to a URL-friendly slug.

    Example: "My Report 01" -> "my-report-01"

    Rules:
    - Convert to lowercase
    - Replace spaces with hyphens
    - Strip leading/trailing whitespace
    """
    return re.sub(r'\s+','-',text.lower().strip())


class ColumnProfile:
    """Represents profiling results for a single column."""

    def __init__(self, name, inferred_type, total, missing, unique):
        """
        Initialize a ColumnProfile.

        Args:
            name: Column name
            inferred_type: "number" or "text"
            total: Total number of rows
            missing: Number of missing values
            unique: Number of unique values
        """
        # YOUR CODE HERE - store the attributes
        self.name = name
        self.inferred_type = inferred_type
        self.total = total
        self.missing = missing
        self.unique = unique

    @property
    def missing_pct(self):
        """Return missing percentage (0-100)."""
        # YOUR CODE HERE
        if self.total == 0:
            return 0.0
        return (self.missing / self.total) * 100

    def to_dict(self):
        """Convert to dictionary for JSON export."""
        # YOUR CODE HERE
        return {
            "name": self.name,
            "type": self.inferred_type,
            "total": self.total,
            "missing": self.missing,
            "missing_pct": self.missing_pct,
            "unique": self.unique,
        }
    def __repr__(self):
        """String representation for debugging."""
        # YOUR CODE HERE
        return (
            f"ColumnProfile(name='{self.name}', "
            f"type='{self.inferred_type}', "
            f"total={self.total}, "
            f"missing={self.missing}, "
            f"unique={self.unique})"
        )
        
        
def build_report(rows):
    if not rows:
        return {"rows": 0, "columns": {}}

    columns = list(rows[0].keys())
    report = {
        "rows": len(rows),
        "columns": {}
    }

    for colname in columns:
        column_items = get_column_from_name(rows, colname)
        report["columns"][colname] = get_column_state(column_items)

    return report


def to_profile(report):
    columns = []
    for name, info in report["columns"].items():
        columns.append({
            "name": name,
            "type": info["type"],
            "missing": info["missing"],
            "unique": info.get("unique", 0),
        })

    return {
        "n_rows": report["rows"],
        "n_cols": len(columns),
        "columns": columns,
    }
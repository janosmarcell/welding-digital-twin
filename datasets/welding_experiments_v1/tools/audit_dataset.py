from pathlib import Path
from collections import Counter, defaultdict
import argparse
import csv
import hashlib
import json
import re
import sys

GROUPS = {
    "g01_30": (1, 30),
    "g02_40": (2, 40),
    "g03_50": (3, 50),
    "g04_60": (4, 60),
    "g05_70": (5, 70),
}

EXPECTED_CSV = 150
EXPECTED_JPG = 20

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dataset",
    default="datasets/welding_experiments_v1"
)
parser.add_argument(
    "--output",
    default="audit-output"
)
args = parser.parse_args()

root = Path(args.dataset)
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)

errors = []
warnings = []
records = []
counts = Counter()
per_group = Counter()
sample_ids = defaultdict(set)
ignored_ply = 0


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(
            lambda: source.read(1024 * 1024), b""
        ):
            digest.update(chunk)
    return digest.hexdigest()


def count_csv_rows(path):
    with path.open(
        "r", encoding="utf-8-sig",
        errors="replace", newline=""
    ) as source:
        sample = source.read(4096)
        source.seek(0)

        delimiter = max(
            [",", ";", "\t"],
            key=lambda char: sample.count(char)
        )
        reader = csv.reader(source, delimiter=delimiter)
        header = next(reader, [])

        if len(header) < 2:
            warnings.append(
                f"Unusual CSV header: {path.name}"
            )

        rows = sum(
            1 for row in reader
            if any(cell.strip() for cell in row)
        )

    return rows


if not root.is_dir():
    errors.append(f"Dataset directory missing: {root}")
else:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        ext = path.suffix.lower()

        if ext == ".ply":
            ignored_ply += 1
            continue

        if ext not in (".csv", ".jpg", ".jpeg"):
            continue

        relative = path.relative_to(root)
        group = relative.parts[0]
        relstr = relative.as_posix()

        file_type = (
            "CSV" if ext == ".csv" else "JPG"
        )
        counts[file_type] += 1

        if group not in GROUPS:
            errors.append(
                f"Unexpected group for {relstr}: {group}"
            )
        elif file_type == "CSV":
            per_group[group] += 1

        match = re.fullmatch(
            r"g(\d{2})_s(\d{2,3})\.(csv|jpg|jpeg)",
            path.name,
            re.IGNORECASE
        )

        sample_id = ""
        if match:
            group_id = int(match.group(1))
            sample_number = int(match.group(2))
            sample_id = (
                f"g{group_id:02d}_s{sample_number:02d}"
            )

            if group in GROUPS:
                expected_group = GROUPS[group][0]
                if group_id != expected_group:
                    errors.append(
                        f"Group mismatch: {relstr}"
                    )

                if file_type == "CSV":
                    lower = (expected_group - 1) * 30 + 1
                    upper = expected_group * 30

                    if not lower <= sample_number <= upper:
                        errors.append(
                            f"Unexpected sample number: {relstr}"
                        )

                    if sample_id in sample_ids[group]:
                        errors.append(
                            f"Duplicate sample ID: {sample_id}"
                        )

                    sample_ids[group].add(sample_id)
        elif file_type == "CSV":
            errors.append(
                f"Unexpected CSV filename: {relstr}"
            )
        else:
            warnings.append(
                f"Image sample ID not resolved: {relstr}"
            )

        size = path.stat().st_size
        if size == 0:
            errors.append(f"Empty file: {relstr}")

        rows = ""
        if file_type == "CSV" and size:
            try:
                rows = count_csv_rows(path)
                if rows == 0:
                    errors.append(f"No CSV data rows: {relstr}")
            except (OSError, UnicodeError, csv.Error) as exc:
                errors.append(
                    f"CSV read error {relstr}: {exc}"
                )

        if file_type == "JPG" and size:
            with path.open("rb") as source:
                if source.read(2) != b"\xff\xd8":
                    errors.append(
                        f"Invalid JPEG signature: {relstr}"
                    )

        records.append({
            "relative_path": relstr,
            "file_type": file_type,
            "sample_id": sample_id,
            "group": group,
            "size_bytes": size,
            "csv_data_rows": rows,
            "sha256": sha256(path)
        })


for group, (group_id, speed) in GROUPS.items():
    if per_group[group] != 30:
        errors.append(
            f"{group}: found {per_group[group]} CSV; expected 30"
        )

    expected_ids = {
        f"g{group_id:02d}_s{n:02d}"
        for n in range((group_id - 1) * 30 + 1,
                       group_id * 30 + 1)
    }

    missing = sorted(expected_ids - sample_ids[group])
    if missing:
        errors.append(
            f"{group} missing samples: {', '.join(missing)}"
        )

if counts["CSV"] != EXPECTED_CSV:
    errors.append(
        f"CSV total: {counts['CSV']}; expected {EXPECTED_CSV}"
    )

if counts["JPG"] != EXPECTED_JPG:
    errors.append(
        f"JPG total: {counts['JPG']}; expected {EXPECTED_JPG}"
    )

fields = [
    "relative_path", "file_type", "sample_id",
    "group", "size_bytes", "csv_data_rows", "sha256"
]

with (output / "manifest.csv").open(
    "w", newline="", encoding="utf-8-sig"
) as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)

with (output / "checksums_sha256.txt").open(
    "w", encoding="utf-8"
) as file:
    for record in records:
        file.write(
            f"{record['sha256']}  "
            f"{record['relative_path']}\n"
        )

status = "FAIL" if errors else "PASS"

summary = {
    "status": status,
    "expected_csv": EXPECTED_CSV,
    "actual_csv": counts["CSV"],
    "expected_jpg": EXPECTED_JPG,
    "actual_jpg": counts["JPG"],
    "ignored_ply": ignored_ply,
    "groups": dict(per_group),
    "errors": errors,
    "warnings": warnings
}

(output / "summary.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

report = [
    "# Welding Dataset v1 Audit",
    "",
    f"**Status:** {status}",
    "",
    f"- CSV: {counts['CSV']} / {EXPECTED_CSV}",
    f"- JPG: {counts['JPG']} / {EXPECTED_JPG}",
    f"- Ignored PLY: {ignored_ply}",
    "",
    "## Group counts",
    ""
]

for group in GROUPS:
    report.append(f"- {group}: {per_group[group]} CSV")

report.extend(["", "## Errors", ""])
report.extend(f"- {item}" for item in errors)
if not errors:
    report.append("None")

report.extend(["", "## Warnings", ""])
report.extend(f"- {item}" for item in warnings)
if not warnings:
    report.append("None")

report.extend([
    "",
    "## Scope",
    "",
    "Structural and file-integrity checks only.",
    "PLY files are excluded.",
    "Weld segmentation, image-to-sample pairing and",
    "weld quality classification are not validated here."
])

(output / "report.md").write_text(
    "\n".join(report) + "\n",
    encoding="utf-8"
)

print(json.dumps(summary, indent=2, ensure_ascii=False))
print(f"Reports saved to: {output}")

sys.exit(1 if errors else 0)

from pathlib import Path
from report.time_utils import today_timezone

REPORT_DIR = Path("reports")
SECTION_ORDER = ["done", "issue", "next", "memo"]
SECTION_LABELS = {
    "done": "今日やったこと",
    "issue": "課題",
    "next": "次にやること",
    "memo": "メモ",
}


def generate_markdown(entries):
    projects = {}
    for entry in entries:
        project = entry.get("project", "").strip()
        section = entry.get("section", "").strip()
        text = entry.get("text", "").strip()

        if not project or section not in SECTION_ORDER or not text:
            continue

        if project not in projects:
            projects[project] = {name: [] for name in SECTION_ORDER}
        projects[project][section].append(text)

    lines = []
    for project in sorted(projects.keys()):
        lines.append(f"- #{project}")
        for section in SECTION_ORDER:
            items = projects[project][section]
            if not items:
                continue
            lines.append(f"    - {SECTION_LABELS[section]}")
            for text in items:
                lines.append(f"        - {text}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n" if lines else ""


def write_daily_report(log_data):
    report_date = log_data.get("date") or today_timezone()
    file_name = report_date.replace("-", "_") + ".md"

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / file_name

    content = generate_markdown(log_data.get("entries", []))
    with report_path.open("w", encoding="utf-8") as f:
        f.write(content)

    return report_path

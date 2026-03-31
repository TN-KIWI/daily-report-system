import argparse
from report.models import Entry
from report import storage
from report import formatter
from report import git_reader
from report import git_entries
from report.git_sources import load_repo_paths


def create_parser():
    parser = argparse.ArgumentParser(description="Daily Report System CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize daily report system")

    add_parser = subparsers.add_parser("add", help="Add a report entry")
    add_parser.add_argument(
        "--section",
        required=True,
        choices=["done", "issue", "next", "memo"],
        help="Section to add the entry to",
    )
    add_parser.add_argument("--project", required=True, help="Project name")
    add_parser.add_argument("text", help="Entry text")

    subparsers.add_parser("generate", help="Generate a report")

    git_log_parser = subparsers.add_parser("git-log", help="Show today's git commit messages")
    git_log_parser.add_argument("--repo", help="Repository path")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "init":
        print("init command called")
    elif args.command == "add":
        try:
            entry = Entry(
                project=args.project,
                section=args.section,
                text=args.text,
            )
            storage.add_entry(entry)
            print("entry saved")
        except Exception as e:
            print(f"failed to save entry: {e}")
    elif args.command == "generate":
        try:
            log_data = storage.load_entries()
            git_log_data = git_entries.load_today_git_entries()
            log_data["entries"] = [*log_data.get("entries", []), *git_log_data]
            report_path = formatter.write_daily_report(log_data)
            print(f"report generated: {report_path}")
        except Exception as e:
            print(f"failed to generate report: {e}")
    elif args.command == "git-log":
        try:
            repo_paths = [args.repo] if args.repo else load_repo_paths()
            has_output = False
            for repo_path in repo_paths:
                messages = git_reader.get_today_commit_messages(repo_path)
                for entry in git_entries.messages_to_entries(repo_path, messages):
                    has_output = True
                    print(entry)
            if not has_output:
                print("no git commits found for today")
        except Exception as e:
            print(f"failed to read git log: {e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

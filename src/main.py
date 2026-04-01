import argparse
from report.models import Entry
from report import storage
from report import formatter
from report import git_reader
from report import git_entries
from report.git_sources import load_repo_paths
from report.time_utils import parse_cli_datetime


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

    generate_parser = subparsers.add_parser("generate", help="Generate a report")
    generate_parser.add_argument("--from", dest="from_dt", help="Start datetime (YYYY-MM-DD HH:MM)")
    generate_parser.add_argument("--to", dest="to_dt", help="End datetime (YYYY-MM-DD HH:MM)")
    generate_parser.add_argument("--output-dir", help="Output directory for report")
    generate_parser.add_argument("--filename", help="Output filename for report")

    git_log_parser = subparsers.add_parser("git-log", help="Show today's git commit messages")
    git_log_parser.add_argument("--repo", help="Repository path")
    git_log_parser.add_argument("--from", dest="from_dt", help="Start datetime (YYYY-MM-DD HH:MM)")
    git_log_parser.add_argument("--to", dest="to_dt", help="End datetime (YYYY-MM-DD HH:MM)")
    return parser


def resolve_datetime_range(args):
    from_arg = getattr(args, "from_dt", None)
    to_arg = getattr(args, "to_dt", None)

    if bool(from_arg) != bool(to_arg):
        raise ValueError("both --from and --to are required together")
    if not from_arg and not to_arg:
        return None, None

    from_dt = parse_cli_datetime(from_arg)
    to_dt = parse_cli_datetime(to_arg)
    if from_dt > to_dt:
        raise ValueError("--from must be earlier than or equal to --to")

    return from_dt.isoformat(), to_dt.isoformat()


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
            from_dt, to_dt = resolve_datetime_range(args)
            log_data = storage.load_entries(from_dt=from_dt, to_dt=to_dt)
            git_log_data = git_entries.load_git_entries(from_dt=from_dt, to_dt=to_dt)
            log_data["entries"] = [*log_data.get("entries", []), *git_log_data]
            report_path = formatter.write_daily_report(
                log_data,
                output_dir=args.output_dir,
                filename=args.filename,
            )
            print(f"report generated: {report_path}")
        except Exception as e:
            print(f"failed to generate report: {e}")
    elif args.command == "git-log":
        try:
            from_dt, to_dt = resolve_datetime_range(args)
            repo_paths = [args.repo] if args.repo else load_repo_paths()
            has_output = False
            for repo_path in repo_paths:
                messages = git_reader.get_commit_messages(repo_path, from_dt=from_dt, to_dt=to_dt)
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

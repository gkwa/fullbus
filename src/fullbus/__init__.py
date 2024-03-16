import argparse
import pathlib
import time

__project_name__ = "fullbus"


def process_file(
    file_path, extensions, excluded_paths, included_paths, timespan, current_time
):
    if any(exclude.lower() in str(file_path).lower() for exclude in excluded_paths):
        return

    if included_paths and not any(
        include.lower() in str(file_path).lower() for include in included_paths
    ):
        return

    if file_path.is_file() and (
        not extensions or file_path.suffix.lower() in extensions
    ):
        modification_time = file_path.stat().st_mtime

        if timespan is None or current_time - modification_time <= timespan:
            print(file_path)


def find_recently_modified_files(
    root_dir, extensions, excluded_paths, included_paths, timespan=None
):
    current_time = time.time()

    try:
        for file_path in root_dir.rglob("*"):
            process_file(
                file_path,
                extensions,
                excluded_paths,
                included_paths,
                timespan,
                current_time,
            )
    except KeyboardInterrupt:
        print("\nQuitting prematurely due to cancellation.")


def parse_timespan(timespan_str):
    unit = timespan_str[-1].lower()
    value = float(timespan_str[:-1])

    if unit == "s":
        return value
    elif unit == "m":
        return value * 60
    elif unit == "h":
        return value * 3600
    elif unit == "d":
        return value * 86400
    else:
        raise ValueError(
            "Invalid timespan format. Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Find recently modified files.")
    parser.add_argument(
        "-t",
        "--timespan",
        type=str,
        help="Timespan for modification (e.g., 5m, 1h, 3.2m, 10s, 2d). If not specified, no timespan limit is applied.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        action="append",
        help="Directories for the search (default: /). Can be specified multiple times.",
    )
    parser.add_argument(
        "-e",
        "--ext",
        action="append",
        help="File extensions to search for",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        action="append",
        help="Paths to exclude from the search",
    )
    parser.add_argument(
        "-i",
        "--include",
        action="append",
        help="Paths to include in the search (case-insensitive)",
    )

    args = parser.parse_args()

    root_directories = args.directory or ["/"]
    file_extensions = [
        ext.lower() if ext.startswith(".") else "." + ext.lower()
        for ext in (args.ext or [])
    ]
    excluded_paths = args.exclude or []
    included_paths = args.include or []
    timespan = parse_timespan(args.timespan) if args.timespan else None

    if not file_extensions:
        print("No file extensions specified. Searching for all files.")
    else:
        print(f"Searching for files with extensions: {', '.join(file_extensions)}")

    if excluded_paths:
        print(f"Excluding paths: {', '.join(excluded_paths)}")

    if included_paths:
        print(f"Including paths: {', '.join(included_paths)}")

    if timespan is None:
        print("No timespan specified. Searching without timespan limit.")
    else:
        print(f"Searching for files modified within the last {args.timespan}.")

    try:
        for root_directory in root_directories:
            print(f"Searching in directory: {root_directory}")
            find_recently_modified_files(
                pathlib.Path(root_directory),
                file_extensions,
                excluded_paths,
                included_paths,
                timespan,
            )
    except KeyboardInterrupt:
        print("\nSearch canceled by the user.")

    return 0

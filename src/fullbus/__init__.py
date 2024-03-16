import argparse
import pathlib
import time

__project_name__ = "fullbus"


def find_recently_modified_files(root_dir, extensions, timespan):
    current_time = time.time()

    for file_path in root_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            modification_time = file_path.stat().st_mtime

            if current_time - modification_time <= timespan:
                print(file_path)


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
        default="5m",
        help="Timespan for modification (e.g., 5m, 1h, 3.2m, 10s, 2d)",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default="/",
        help="Starting directory for the search (default: /)",
    )
    parser.add_argument(
        "-e",
        "--ext",
        action="append",
        help="File extensions to search for",
    )
    args = parser.parse_args()

    root_directory = pathlib.Path(args.directory)
    file_extensions = [
        ext.lower() if ext.startswith(".") else "." + ext.lower() for ext in (args.ext or [])
    ]
    timespan = parse_timespan(args.timespan)

    if not file_extensions:
        print("No file extensions specified. Searching for all files.")
    else:
        print(f"Searching for files with extensions: {', '.join(file_extensions)}")

    find_recently_modified_files(root_directory, file_extensions, timespan)

    return 0
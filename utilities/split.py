#!/usr/bin/env python3

# ./split.py hi.pck --parts 4
# or no larger than NM : ./split.py hi.pck --max-size 5M
# ./split.py hi.pck --combine to combine


import os
import sys
import argparse
from math import ceil

def split_file(filename, max_size=None, parts=None):
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    filesize = os.path.getsize(filename)
    print(f"Splitting '{filename}' ({filesize:,} bytes)")

    if parts:
        part_size = ceil(filesize / parts)
    elif max_size:
        part_size = max_size
        parts = ceil(filesize / part_size)
    else:
        print("Error: must specify either --max-size or --parts.")
        sys.exit(1)

    with open(filename, "rb") as f:
        for i in range(parts):
            part_filename = f"{filename}.part{i+1}"
            with open(part_filename, "wb") as pf:
                chunk = f.read(part_size)
                pf.write(chunk)
                print(f"Created: {part_filename} ({len(chunk):,} bytes)")

    print("✅ Split complete!")


def combine_file(base_filename):
    part_files = sorted(
        [f for f in os.listdir('.') if f.startswith(base_filename + ".part")],
        key=lambda x: int(x.split("part")[-1])
    )

    if not part_files:
        print(f"No parts found for '{base_filename}'.")
        sys.exit(1)

    output_filename = base_filename
    with open(output_filename, "wb") as outfile:
        for part in part_files:
            with open(part, "rb") as pf:
                data = pf.read()
                outfile.write(data)
                print(f"Added: {part} ({len(data):,} bytes)")

    print(f"✅ Combined into '{output_filename}'")


def parse_size(size_str):
    """Convert human-readable size strings like 10M, 512K, etc."""
    size_str = size_str.strip().upper()
    if size_str.endswith('K'):
        return int(float(size_str[:-1]) * 1024)
    elif size_str.endswith('M'):
        return int(float(size_str[:-1]) * 1024**2)
    elif size_str.endswith('G'):
        return int(float(size_str[:-1]) * 1024**3)
    else:
        return int(size_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split and combine files easily.")
    parser.add_argument("file", help="File to split or base name to combine.")
    parser.add_argument("--max-size", help="Max part size (e.g., 10M, 512K).")
    parser.add_argument("--parts", type=int, help="Number of parts to split into.")
    parser.add_argument("--combine", action="store_true", help="Combine parts back together.")
    args = parser.parse_args()

    if args.combine:
        combine_file(args.file)
    else:
        max_size = parse_size(args.max_size) if args.max_size else None
        split_file(args.file, max_size=max_size, parts=args.parts)

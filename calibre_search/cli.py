"""
Command-line interface for Calibre search tool.

This module provides the CLI for searching Calibre databases
and generating markdown catalogs.
"""

import argparse
import os
import sys
from typing import Dict, Optional

from .db import create_readonly_copy, search_database, cleanup_readonly_copy
from .query import build_query
from .report import generate_markdown


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Search Calibre metadata.db and generate a markdown catalog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --author "Mark Lutz"
  %(prog)s --title "Python" --format PDF
  %(prog)s --author "Lutz" --output my_books.md
  %(prog)s --publisher "O'Reilly" --format EPUB
  %(prog)s --series "Head First" --tag "Programming"
  %(prog)s --database /path/to/custom/metadata.db
        """
    )

    parser.add_argument(
        '--database', '-d',
        default=os.path.expanduser('~/Calibre/metadata.db'),
        help='Path to Calibre metadata.db (default: ~/Calibre/metadata.db)'
    )

    parser.add_argument(
        '--output', '-o',
        default='catalog.md',
        help='Output markdown file (default: catalog.md)'
    )

    parser.add_argument(
        '--title', '-t',
        help='Search by title (case-insensitive, partial match)'
    )

    parser.add_argument(
        '--author', '-a',
        help='Search by author (case-insensitive, partial match)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['PDF', 'EPUB', 'AZW3', 'MOBI', 'PRC', 'ORIGINAL_AZW3', 'ORIGINAL_EPUB'],
        help='Filter by format'
    )

    parser.add_argument(
        '--publisher', '-p',
        help='Search by publisher (case-insensitive, partial match)'
    )

    parser.add_argument(
        '--series', '-s',
        help='Search by series (case-insensitive, partial match)'
    )

    parser.add_argument(
        '--tag',
        help='Search by tag (case-insensitive, partial match)'
    )

    parser.add_argument(
        '--no-copy',
        action='store_true',
        help='Skip creating readonly copy (use original database directly)'
    )

    return parser.parse_args()


def build_search_filters(args: argparse.Namespace) -> Dict[str, Optional[str]]:
    """
    Build search filters dictionary from command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Dictionary of search filters
    """
    return {
        'title': args.title,
        'author': args.author,
        'format': args.format,
        'publisher': args.publisher,
        'series': args.series,
        'tag': args.tag
    }


def validate_database(db_path: str) -> bool:
    """
    Validate that the database file exists.

    Args:
        db_path: Path to the database file

    Returns:
        True if database exists, False otherwise
    """
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found", file=sys.stderr)
        return False
    return True


def main() -> int:
    """
    Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_arguments()

    # Expand user paths
    args.database = os.path.expanduser(args.database)
    args.output = os.path.expanduser(args.output)

    # Validate database exists
    if not validate_database(args.database):
        return 1

    # Determine database path to use
    readonly_db = None
    if args.no_copy:
        db_path = args.database
        print(f"Using original database: {db_path}")
    else:
        readonly_db = args.database + '.readonly'
        try:
            db_path = create_readonly_copy(args.database, readonly_db)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error creating readonly copy: {e}", file=sys.stderr)
            return 1

    try:
        # Build search filters
        search_filters = build_search_filters(args)

        # Build query
        query, params = build_query(search_filters)
        print(f"Executing query with filters: {search_filters}")

        # Search database
        results, total_books = search_database(db_path, query, params)
        print(f"Found {len(results)} books matching criteria")

        # Generate markdown output
        generate_markdown(results, args.output, search_filters, total_books)

        print(f"\nSuccess! Catalog saved to: {args.output}")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    finally:
        # Clean up readonly copy
        if readonly_db:
            cleanup_readonly_copy(readonly_db)


if __name__ == '__main__':
    sys.exit(main())

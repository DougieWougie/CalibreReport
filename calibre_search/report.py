"""
Markdown report generation for Calibre search results.

This module handles formatting and writing search results to markdown files.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple


class MarkdownReportGenerator:
    """Generator for creating markdown reports from Calibre search results."""

    def __init__(
        self,
        results: List[Tuple],
        search_filters: Dict[str, Optional[str]],
        total_books: int
    ):
        """
        Initialize the report generator.

        Args:
            results: List of search result tuples (title, authors, formats)
            search_filters: Dictionary of applied search filters
            total_books: Total number of books in the database
        """
        self.results = results
        self.search_filters = search_filters
        self.total_books = total_books

    def _write_header(self, f) -> None:
        """Write the markdown header."""
        f.write("# Calibre eBook Catalog\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    def _write_filters(self, f) -> None:
        """Write the search filters section."""
        if any(self.search_filters.values()):
            f.write("## Search Filters\n\n")
            for key, value in self.search_filters.items():
                if value:
                    f.write(f"- **{key.capitalize()}**: {value}\n")
            f.write("\n")

    def _write_statistics(self, f) -> None:
        """Write the statistics section."""
        f.write("## Statistics\n\n")
        f.write(f"- Total books in database: {self.total_books}\n")
        f.write(f"- Books matching filters: {len(self.results)}\n\n")

    def _escape_markdown(self, text: str) -> str:
        """
        Escape special markdown characters in text.

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for markdown table
        """
        return text.replace('|', '\\|')

    def _write_results_table(self, f) -> None:
        """Write the results table."""
        f.write("## Books\n\n")
        f.write("| Title | Author | Formats |\n")
        f.write("|-------|--------|----------|\n")

        for row in self.results:
            title = row[0] if row[0] else "Unknown"
            authors = row[1] if row[1] else "Unknown"
            formats = row[2] if row[2] else "None"

            # Escape special characters
            title = self._escape_markdown(title)
            authors = self._escape_markdown(authors)
            formats = self._escape_markdown(formats)

            f.write(f"| {title} | {authors} | {formats} |\n")

    def _write_footer(self, f) -> None:
        """Write the markdown footer."""
        f.write(f"\n---\n*Generated from Calibre metadata.db*\n")

    def generate(self, output_file: str) -> None:
        """
        Generate and write the markdown report.

        Args:
            output_file: Path to the output markdown file

        Raises:
            IOError: If unable to write to the output file
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            self._write_header(f)
            self._write_filters(f)
            self._write_statistics(f)
            self._write_results_table(f)
            self._write_footer(f)

        print(f"Markdown file generated: {output_file}")


def generate_markdown(
    results: List[Tuple],
    output_file: str,
    search_filters: Dict[str, Optional[str]],
    total_books: int
) -> None:
    """
    Generate markdown file from search results.

    Args:
        results: List of search result tuples (title, authors, formats)
        output_file: Path to the output markdown file
        search_filters: Dictionary of applied search filters
        total_books: Total number of books in the database

    Example:
        >>> results = [('Book Title', 'Author Name', 'PDF, EPUB')]
        >>> filters = {'author': 'Author Name'}
        >>> generate_markdown(results, 'catalog.md', filters, 100)
    """
    generator = MarkdownReportGenerator(results, search_filters, total_books)
    generator.generate(output_file)

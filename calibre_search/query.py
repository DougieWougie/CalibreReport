"""
SQL query builder for Calibre database searches.

This module constructs SQL queries based on search filters.
"""

from typing import Dict, List, Optional, Tuple


class QueryBuilder:
    """Builder for constructing SQL queries for Calibre database searches."""

    BASE_QUERY = """
    SELECT
        b.title,
        GROUP_CONCAT(a.name, ', ') as authors,
        GROUP_CONCAT(d.format, ', ') as formats
    FROM books b
    LEFT JOIN books_authors_link bal ON b.id = bal.book
    LEFT JOIN authors a ON bal.author = a.id
    LEFT JOIN data d ON b.id = d.book
    """

    def __init__(self, search_filters: Dict[str, Optional[str]]):
        """
        Initialize the query builder.

        Args:
            search_filters: Dictionary of search filters
                (title, author, format, publisher, series, tag)
        """
        self.search_filters = search_filters
        self.conditions = []
        self.params = []
        self.query = self.BASE_QUERY

    def _add_title_filter(self) -> None:
        """Add title filter to the query."""
        if self.search_filters.get('title'):
            self.conditions.append("b.title LIKE ?")
            self.params.append(f"%{self.search_filters['title']}%")

    def _add_author_filter(self) -> None:
        """Add author filter to the query."""
        if self.search_filters.get('author'):
            self.conditions.append("a.name LIKE ?")
            self.params.append(f"%{self.search_filters['author']}%")

    def _add_format_filter(self) -> None:
        """Add format filter to the query."""
        if self.search_filters.get('format'):
            self.conditions.append("d.format = ?")
            self.params.append(self.search_filters['format'].upper())

    def _add_publisher_filter(self) -> None:
        """Add publisher filter and necessary joins to the query."""
        if self.search_filters.get('publisher'):
            self.query = self.query.replace(
                "LEFT JOIN data d ON b.id = d.book",
                """LEFT JOIN data d ON b.id = d.book
            LEFT JOIN books_publishers_link bpl ON b.id = bpl.book
            LEFT JOIN publishers p ON bpl.publisher = p.id"""
            )
            self.conditions.append("p.name LIKE ?")
            self.params.append(f"%{self.search_filters['publisher']}%")

    def _add_series_filter(self) -> None:
        """Add series filter and necessary joins to the query."""
        if self.search_filters.get('series'):
            self.query = self.query.replace(
                "LEFT JOIN data d ON b.id = d.book",
                """LEFT JOIN data d ON b.id = d.book
            LEFT JOIN books_series_link bsl ON b.id = bsl.book
            LEFT JOIN series s ON bsl.series = s.id"""
            )
            self.conditions.append("s.name LIKE ?")
            self.params.append(f"%{self.search_filters['series']}%")

    def _add_tag_filter(self) -> None:
        """Add tag filter and necessary joins to the query."""
        if self.search_filters.get('tag'):
            self.query = self.query.replace(
                "LEFT JOIN data d ON b.id = d.book",
                """LEFT JOIN data d ON b.id = d.book
            LEFT JOIN books_tags_link btl ON b.id = btl.book
            LEFT JOIN tags t ON btl.tag = t.id"""
            )
            self.conditions.append("t.name LIKE ?")
            self.params.append(f"%{self.search_filters['tag']}%")

    def build(self) -> Tuple[str, List]:
        """
        Build the complete SQL query with all filters.

        Returns:
            Tuple of (query string, parameters list)
        """
        # Add all filters
        self._add_title_filter()
        self._add_author_filter()
        self._add_format_filter()
        self._add_publisher_filter()
        self._add_series_filter()
        self._add_tag_filter()

        # Add WHERE clause if there are conditions
        if self.conditions:
            self.query += " WHERE " + " AND ".join(self.conditions)

        # Add GROUP BY and ORDER BY
        self.query += " GROUP BY b.title ORDER BY b.title"

        return self.query, self.params


def build_query(search_filters: Dict[str, Optional[str]]) -> Tuple[str, List]:
    """
    Build SQL query based on search filters.

    Args:
        search_filters: Dictionary of search filters
            (title, author, format, publisher, series, tag)

    Returns:
        Tuple of (query string, parameters list)

    Example:
        >>> filters = {'title': 'Python', 'author': 'Lutz'}
        >>> query, params = build_query(filters)
    """
    builder = QueryBuilder(search_filters)
    return builder.build()

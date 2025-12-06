"""Unit tests for the CLI module."""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from calibre_search.cli import (
    build_search_filters,
    validate_database,
    parse_arguments
)


class TestBuildSearchFilters(unittest.TestCase):
    """Test cases for build_search_filters function."""

    def test_build_filters_all_fields(self):
        """Test building filters with all fields present."""
        args = MagicMock()
        args.title = 'Python'
        args.author = 'Lutz'
        args.format = 'PDF'
        args.publisher = "O'Reilly"
        args.series = 'Head First'
        args.tag = 'Programming'

        filters = build_search_filters(args)

        self.assertEqual(filters['title'], 'Python')
        self.assertEqual(filters['author'], 'Lutz')
        self.assertEqual(filters['format'], 'PDF')
        self.assertEqual(filters['publisher'], "O'Reilly")
        self.assertEqual(filters['series'], 'Head First')
        self.assertEqual(filters['tag'], 'Programming')

    def test_build_filters_partial_fields(self):
        """Test building filters with some fields None."""
        args = MagicMock()
        args.title = 'Python'
        args.author = None
        args.format = None
        args.publisher = None
        args.series = None
        args.tag = None

        filters = build_search_filters(args)

        self.assertEqual(filters['title'], 'Python')
        self.assertIsNone(filters['author'])
        self.assertIsNone(filters['format'])


class TestValidateDatabase(unittest.TestCase):
    """Test cases for validate_database function."""

    def test_validate_existing_database(self):
        """Test validation with existing database."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_db = f.name

        try:
            result = validate_database(temp_db)
            self.assertTrue(result)
        finally:
            os.remove(temp_db)

    def test_validate_nonexistent_database(self):
        """Test validation with nonexistent database."""
        result = validate_database('/nonexistent/path/metadata.db')
        self.assertFalse(result)


class TestParseArguments(unittest.TestCase):
    """Test cases for parse_arguments function."""

    def test_parse_default_arguments(self):
        """Test parsing with default arguments."""
        with patch('sys.argv', ['calibre-search']):
            args = parse_arguments()

            self.assertTrue(args.database.endswith('metadata.db'))
            self.assertEqual(args.output, 'catalog.md')
            self.assertIsNone(args.title)
            self.assertIsNone(args.author)
            self.assertFalse(args.no_copy)

    def test_parse_custom_arguments(self):
        """Test parsing with custom arguments."""
        test_args = [
            'calibre-search',
            '--database', '/custom/path/metadata.db',
            '--output', 'my_catalog.md',
            '--title', 'Python',
            '--author', 'Lutz',
            '--format', 'PDF',
            '--no-copy'
        ]

        with patch('sys.argv', test_args):
            args = parse_arguments()

            self.assertEqual(args.database, '/custom/path/metadata.db')
            self.assertEqual(args.output, 'my_catalog.md')
            self.assertEqual(args.title, 'Python')
            self.assertEqual(args.author, 'Lutz')
            self.assertEqual(args.format, 'PDF')
            self.assertTrue(args.no_copy)

    def test_parse_short_arguments(self):
        """Test parsing with short argument flags."""
        test_args = [
            'calibre-search',
            '-d', '/path/to/db',
            '-o', 'output.md',
            '-t', 'Title',
            '-a', 'Author',
            '-f', 'EPUB'
        ]

        with patch('sys.argv', test_args):
            args = parse_arguments()

            self.assertEqual(args.database, '/path/to/db')
            self.assertEqual(args.output, 'output.md')
            self.assertEqual(args.title, 'Title')
            self.assertEqual(args.author, 'Author')
            self.assertEqual(args.format, 'EPUB')


if __name__ == '__main__':
    unittest.main()

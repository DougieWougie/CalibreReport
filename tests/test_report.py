"""Unit tests for the report module."""

import os
import tempfile
import unittest
from calibre_search.report import MarkdownReportGenerator, generate_markdown


class TestMarkdownReportGenerator(unittest.TestCase):
    """Test cases for MarkdownReportGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.temp_dir, 'test_report.md')

        self.test_results = [
            ('Python Programming', 'Mark Lutz', 'PDF, EPUB'),
            ('Learning Python', 'Mark Lutz', 'PDF'),
            ('Test | Book', 'Author | Name', 'MOBI')
        ]

        self.test_filters = {
            'title': 'Python',
            'author': None,
            'format': None,
            'publisher': None,
            'series': None,
            'tag': None
        }

        self.total_books = 100

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        try:
            os.rmdir(self.temp_dir)
        except:
            pass

    def test_generate_report(self):
        """Test basic report generation."""
        generator = MarkdownReportGenerator(
            self.test_results,
            self.test_filters,
            self.total_books
        )
        generator.generate(self.output_file)

        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('# Calibre eBook Catalog', content)
        self.assertIn('Generated:', content)
        self.assertIn('## Statistics', content)
        self.assertIn('Total books in database: 100', content)
        self.assertIn('Books matching filters: 3', content)
        self.assertIn('## Books', content)
        self.assertIn('Python Programming', content)
        self.assertIn('Mark Lutz', content)

    def test_report_with_filters(self):
        """Test report generation with multiple filters."""
        filters = {
            'title': 'Python',
            'author': 'Lutz',
            'format': 'PDF',
            'publisher': None,
            'series': None,
            'tag': None
        }
        generator = MarkdownReportGenerator(
            self.test_results,
            filters,
            self.total_books
        )
        generator.generate(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('## Search Filters', content)
        self.assertIn('**Title**: Python', content)
        self.assertIn('**Author**: Lutz', content)
        self.assertIn('**Format**: PDF', content)

    def test_report_without_filters(self):
        """Test report generation without filters."""
        filters = {k: None for k in self.test_filters.keys()}
        generator = MarkdownReportGenerator(
            self.test_results,
            filters,
            self.total_books
        )
        generator.generate(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertNotIn('## Search Filters', content)

    def test_escape_markdown(self):
        """Test markdown character escaping."""
        generator = MarkdownReportGenerator([], {}, 0)

        # Test pipe character escaping
        escaped = generator._escape_markdown('Text | with | pipes')
        self.assertEqual(escaped, 'Text \\| with \\| pipes')

        # Test text without special characters
        escaped = generator._escape_markdown('Normal text')
        self.assertEqual(escaped, 'Normal text')

    def test_pipe_escaping_in_results(self):
        """Test that pipe characters in results are escaped."""
        generator = MarkdownReportGenerator(
            self.test_results,
            self.test_filters,
            self.total_books
        )
        generator.generate(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that pipes are escaped in the table
        self.assertIn('Test \\| Book', content)
        self.assertIn('Author \\| Name', content)

    def test_empty_results(self):
        """Test report generation with no results."""
        generator = MarkdownReportGenerator(
            [],
            self.test_filters,
            self.total_books
        )
        generator.generate(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('Books matching filters: 0', content)
        self.assertIn('| Title | Author | Formats |', content)

    def test_null_values_in_results(self):
        """Test handling of None/null values in results."""
        results_with_nulls = [
            (None, None, None),
            ('Title', None, 'PDF'),
            ('Another', 'Author', None)
        ]
        generator = MarkdownReportGenerator(
            results_with_nulls,
            {},
            10
        )
        generator.generate(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('Unknown', content)
        self.assertIn('None', content)


class TestGenerateMarkdown(unittest.TestCase):
    """Test cases for generate_markdown function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.temp_dir, 'test_catalog.md')

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        try:
            os.rmdir(self.temp_dir)
        except:
            pass

    def test_generate_markdown_function(self):
        """Test the generate_markdown convenience function."""
        results = [('Book', 'Author', 'PDF')]
        filters = {'title': 'Book'}
        total_books = 50

        generate_markdown(results, self.output_file, filters, total_books)

        self.assertTrue(os.path.exists(self.output_file))


if __name__ == '__main__':
    unittest.main()

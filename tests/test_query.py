"""Unit tests for the query module."""

import unittest
from calibre_search.query import QueryBuilder, build_query


class TestQueryBuilder(unittest.TestCase):
    """Test cases for QueryBuilder class."""

    def test_empty_filters(self):
        """Test query with no filters."""
        builder = QueryBuilder({})
        query, params = builder.build()

        self.assertIn("SELECT", query)
        self.assertIn("FROM books b", query)
        self.assertIn("GROUP BY b.title ORDER BY b.title", query)
        self.assertNotIn("WHERE", query)
        self.assertEqual(params, [])

    def test_title_filter(self):
        """Test query with title filter."""
        filters = {'title': 'Python'}
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("b.title LIKE ?", query)
        self.assertEqual(params, ['%Python%'])

    def test_author_filter(self):
        """Test query with author filter."""
        filters = {'author': 'Lutz'}
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("a.name LIKE ?", query)
        self.assertEqual(params, ['%Lutz%'])

    def test_format_filter(self):
        """Test query with format filter."""
        filters = {'format': 'pdf'}
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("d.format = ?", query)
        self.assertEqual(params, ['PDF'])

    def test_publisher_filter(self):
        """Test query with publisher filter."""
        filters = {'publisher': "O'Reilly"}
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("p.name LIKE ?", query)
        self.assertIn("LEFT JOIN books_publishers_link", query)
        self.assertIn("LEFT JOIN publishers p", query)
        self.assertEqual(params, ["%O'Reilly%"])

    def test_series_filter(self):
        """Test query with series filter."""
        filters = {'series': 'Head First'}
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("s.name LIKE ?", query)
        self.assertIn("LEFT JOIN books_series_link", query)
        self.assertIn("LEFT JOIN series s", query)
        self.assertEqual(params, ['%Head First%'])

    def test_tag_filter(self):
        """Test query with tag filter."""
        filters = {'tag': 'Programming'}
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("t.name LIKE ?", query)
        self.assertIn("LEFT JOIN books_tags_link", query)
        self.assertIn("LEFT JOIN tags t", query)
        self.assertEqual(params, ['%Programming%'])

    def test_multiple_filters(self):
        """Test query with multiple filters."""
        filters = {
            'title': 'Python',
            'author': 'Lutz',
            'format': 'PDF'
        }
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("WHERE", query)
        self.assertIn("b.title LIKE ?", query)
        self.assertIn("a.name LIKE ?", query)
        self.assertIn("d.format = ?", query)
        self.assertIn("AND", query)
        self.assertEqual(len(params), 3)
        self.assertEqual(params, ['%Python%', '%Lutz%', 'PDF'])

    def test_none_values_ignored(self):
        """Test that None filter values are ignored."""
        filters = {
            'title': 'Python',
            'author': None,
            'format': None
        }
        builder = QueryBuilder(filters)
        query, params = builder.build()

        self.assertIn("b.title LIKE ?", query)
        self.assertNotIn("a.name LIKE ?", query)
        self.assertNotIn("d.format = ?", query)
        self.assertEqual(len(params), 1)


class TestBuildQuery(unittest.TestCase):
    """Test cases for build_query function."""

    def test_build_query_function(self):
        """Test the build_query convenience function."""
        filters = {'title': 'Python', 'author': 'Lutz'}
        query, params = build_query(filters)

        self.assertIsInstance(query, str)
        self.assertIsInstance(params, list)
        self.assertIn("SELECT", query)
        self.assertEqual(len(params), 2)


if __name__ == '__main__':
    unittest.main()

"""Unit tests for the database module."""

import os
import sqlite3
import tempfile
import unittest
from calibre_search.db import (
    create_readonly_copy,
    search_database,
    cleanup_readonly_copy
)


class TestDatabaseOperations(unittest.TestCase):
    """Test cases for database operations."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary test database
        self.temp_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.temp_dir, 'test_metadata.db')
        self.readonly_db = self.test_db + '.readonly'

        # Create a simple test database
        self._create_test_database()

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove test databases
        for db_file in [self.test_db, self.readonly_db]:
            if os.path.exists(db_file):
                try:
                    os.chmod(db_file, 0o644)
                    os.remove(db_file)
                except:
                    pass

        # Remove temp directory
        try:
            os.rmdir(self.temp_dir)
        except:
            pass

    def _create_test_database(self):
        """Create a minimal Calibre-like test database."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()

        # Create books table
        cursor.execute("""
            CREATE TABLE books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )
        """)

        # Create authors table
        cursor.execute("""
            CREATE TABLE authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        # Create books_authors_link table
        cursor.execute("""
            CREATE TABLE books_authors_link (
                id INTEGER PRIMARY KEY,
                book INTEGER NOT NULL,
                author INTEGER NOT NULL
            )
        """)

        # Create data table
        cursor.execute("""
            CREATE TABLE data (
                id INTEGER PRIMARY KEY,
                book INTEGER NOT NULL,
                format TEXT NOT NULL
            )
        """)

        # Insert test data
        cursor.execute("INSERT INTO books (id, title) VALUES (1, 'Test Book')")
        cursor.execute("INSERT INTO authors (id, name) VALUES (1, 'Test Author')")
        cursor.execute("INSERT INTO books_authors_link (book, author) VALUES (1, 1)")
        cursor.execute("INSERT INTO data (book, format) VALUES (1, 'PDF')")

        conn.commit()
        conn.close()

    def test_create_readonly_copy_success(self):
        """Test successful creation of readonly copy."""
        result = create_readonly_copy(self.test_db, self.readonly_db)

        self.assertEqual(result, self.readonly_db)
        self.assertTrue(os.path.exists(self.readonly_db))

        # Check that the file is readonly
        mode = os.stat(self.readonly_db).st_mode
        self.assertEqual(mode & 0o777, 0o444)

    def test_create_readonly_copy_nonexistent_source(self):
        """Test creating readonly copy with nonexistent source."""
        nonexistent = os.path.join(self.temp_dir, 'nonexistent.db')

        with self.assertRaises(FileNotFoundError):
            create_readonly_copy(nonexistent, self.readonly_db)

    def test_search_database_basic(self):
        """Test basic database search."""
        query = """
        SELECT b.title, a.name, d.format
        FROM books b
        LEFT JOIN books_authors_link bal ON b.id = bal.book
        LEFT JOIN authors a ON bal.author = a.id
        LEFT JOIN data d ON b.id = d.book
        """
        params = []

        results, total = search_database(self.test_db, query, params)

        self.assertIsInstance(results, list)
        self.assertGreater(total, 0)
        self.assertEqual(total, 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 'Test Book')

    def test_search_database_with_params(self):
        """Test database search with parameters."""
        query = """
        SELECT b.title
        FROM books b
        WHERE b.title LIKE ?
        """
        params = ['%Test%']

        results, total = search_database(self.test_db, query, params)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 'Test Book')

    def test_cleanup_readonly_copy(self):
        """Test cleanup of readonly database."""
        create_readonly_copy(self.test_db, self.readonly_db)
        self.assertTrue(os.path.exists(self.readonly_db))

        cleanup_readonly_copy(self.readonly_db)
        self.assertFalse(os.path.exists(self.readonly_db))

    def test_cleanup_nonexistent_file(self):
        """Test cleanup of nonexistent file (should not raise error)."""
        nonexistent = os.path.join(self.temp_dir, 'nonexistent.db')
        cleanup_readonly_copy(nonexistent)


if __name__ == '__main__':
    unittest.main()

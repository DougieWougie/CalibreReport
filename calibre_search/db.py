"""
Database operations for Calibre metadata.

This module handles database connection, readonly copy creation,
and search operations.
"""

import os
import shutil
import sqlite3
from typing import Dict, List, Optional, Tuple


def create_readonly_copy(source_db: str, readonly_db: str) -> str:
    """
    Create a readonly copy of the database.

    Args:
        source_db: Path to the source database file
        readonly_db: Path for the readonly copy

    Returns:
        Path to the readonly database

    Raises:
        FileNotFoundError: If source database doesn't exist
        PermissionError: If unable to create copy or change permissions
    """
    if not os.path.exists(source_db):
        raise FileNotFoundError(f"Source database not found: {source_db}")

    print(f"Creating readonly copy: {source_db} -> {readonly_db}")
    shutil.copy2(source_db, readonly_db)
    os.chmod(readonly_db, 0o444)
    return readonly_db


def search_database(
    db_path: str,
    query: str,
    params: List
) -> Tuple[List[Tuple], int]:
    """
    Execute a search query on the Calibre database.

    Args:
        db_path: Path to the database file
        query: SQL query string
        params: Query parameters

    Returns:
        Tuple of (search results, total book count)

    Raises:
        sqlite3.Error: If database query fails
    """
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cursor = conn.cursor()

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Get total book count
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]

        return results, total_books
    finally:
        conn.close()


def cleanup_readonly_copy(readonly_db: str) -> None:
    """
    Remove a readonly database copy.

    Args:
        readonly_db: Path to the readonly database to remove
    """
    if os.path.exists(readonly_db):
        os.chmod(readonly_db, 0o644)
        os.remove(readonly_db)
        print(f"Cleaned up readonly copy: {readonly_db}")

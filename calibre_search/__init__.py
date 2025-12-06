"""
Calibre Database Search Tool

A Python package for searching Calibre metadata databases and generating
markdown catalogs of ebooks.
"""

__version__ = '1.0.0'

from .db import create_readonly_copy, search_database
from .query import build_query
from .report import generate_markdown

__all__ = [
    'create_readonly_copy',
    'search_database',
    'build_query',
    'generate_markdown',
]

# Quick Start Guide

## Installation

```bash
cd /home/dougie/Projects/claude/calibre_report
pip install -e .
```

## Running Tests

```bash
python3 -m unittest discover tests -v
```

Expected output: `Ran 31 tests in X.XXXs - OK`

## Basic Usage

### 1. Search all books
```bash
python3 -m calibre_search.cli
```

### 2. Search by author
```bash
python3 -m calibre_search.cli --author "Mark Lutz"
```

### 3. Search by title and format
```bash
python3 -m calibre_search.cli --title "Python" --format PDF
```

### 4. Custom output file
```bash
python3 -m calibre_search.cli --output my_catalog.md
```

### 5. Multiple filters
```bash
python3 -m calibre_search.cli --author "Lutz" --format PDF --publisher "O'Reilly"
```

## Using as a Python Library

```python
from calibre_search import build_query, search_database, generate_markdown

# Define filters
filters = {
    'title': 'Python',
    'author': 'Lutz',
    'format': 'PDF',
    'publisher': None,
    'series': None,
    'tag': None
}

# Build and execute query
query, params = build_query(filters)
results, total_books = search_database('/path/to/metadata.db', query, params)

# Generate report
generate_markdown(results, 'output.md', filters, total_books)
```

## Project Structure

```
calibre_search/          # Main package
├── __init__.py         # Package exports
├── cli.py              # Command-line interface
├── db.py               # Database operations
├── query.py            # SQL query building
└── report.py           # Report generation

tests/                   # Test suite
├── test_cli.py
├── test_db.py
├── test_query.py
└── test_report.py
```

## Module Overview

### calibre_search.db
- `create_readonly_copy(source, dest)` - Create safe readonly database copy
- `search_database(path, query, params)` - Execute search query
- `cleanup_readonly_copy(path)` - Remove readonly copy

### calibre_search.query
- `QueryBuilder(filters)` - Build SQL queries with filters
- `build_query(filters)` - Convenience function for building queries

### calibre_search.report
- `MarkdownReportGenerator(results, filters, total)` - Generate markdown reports
- `generate_markdown(results, file, filters, total)` - Convenience function

### calibre_search.cli
- `main()` - Entry point for command-line interface
- `parse_arguments()` - Parse CLI arguments
- `build_search_filters(args)` - Build filter dict from args

## Help

```bash
python3 -m calibre_search.cli --help
```

## Common Tasks

### View test coverage
```bash
# Install coverage first
pip install coverage

# Run with coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Creates htmlcov/index.html
```

### Run specific test
```bash
python3 -m unittest tests.test_query.TestQueryBuilder.test_title_filter
```

### Format code (if black is installed)
```bash
pip install black
black calibre_search/ tests/
```

### Lint code (if flake8 is installed)
```bash
pip install flake8
flake8 calibre_search/ tests/
```

## Troubleshooting

**Database not found?**
```bash
# Specify custom path
python3 -m calibre_search.cli --database /path/to/metadata.db
```

**Permission errors?**
```bash
# Skip readonly copy
python3 -m calibre_search.cli --no-copy
```

**Import errors?**
```bash
# Make sure you're in the project directory
cd /home/dougie/Projects/claude/calibre_report

# Or install the package
pip install -e .
```

## More Information

- Full documentation: [README.md](README.md)
- Refactoring details: [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)

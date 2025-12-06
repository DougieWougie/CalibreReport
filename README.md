# Calibre Search

A Python package for searching Calibre metadata databases and generating markdown catalogs of ebooks.

## Features

- Search Calibre ebook library by title, author, format, publisher, series, or tag
- Generate formatted markdown catalogs of search results
- Safe readonly database access with automatic cleanup
- Comprehensive test coverage
- Clean modular architecture

## Installation

### From source

```bash
cd calibre_report
pip install -e .
```

### Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Usage

### Command Line Interface

#### Basic usage (all books in catalog)

```bash
python -m calibre_search.cli
```

#### Search by author

```bash
python -m calibre_search.cli --author "Mark Lutz"
```

#### Search by title and format

```bash
python -m calibre_search.cli --title "Python" --format PDF
```

#### Custom database and output file

```bash
python -m calibre_search.cli --database ~/MyLibrary/metadata.db --output my_books.md
```

#### Multiple filters

```bash
python -m calibre_search.cli --publisher "O'Reilly" --format EPUB --tag "Programming"
```

#### Search by series

```bash
python -m calibre_search.cli --series "Head First"
```

### Command Line Options

```
  -h, --help            Show help message and exit
  --database, -d PATH   Path to Calibre metadata.db (default: ~/Calibre/metadata.db)
  --output, -o FILE     Output markdown file (default: catalog.md)
  --title, -t TEXT      Search by title (case-insensitive, partial match)
  --author, -a TEXT     Search by author (case-insensitive, partial match)
  --format, -f FORMAT   Filter by format (PDF, EPUB, AZW3, MOBI, etc.)
  --publisher, -p TEXT  Search by publisher (case-insensitive, partial match)
  --series, -s TEXT     Search by series (case-insensitive, partial match)
  --tag TEXT            Search by tag (case-insensitive, partial match)
  --no-copy             Skip creating readonly copy (use original database)
```

### Programmatic Usage

You can also use the package programmatically in your Python code:

```python
from calibre_search import build_query, search_database, generate_markdown

# Define search filters
filters = {
    'title': 'Python',
    'author': 'Lutz',
    'format': 'PDF',
    'publisher': None,
    'series': None,
    'tag': None
}

# Build query
query, params = build_query(filters)

# Search database
results, total_books = search_database('/path/to/metadata.db', query, params)

# Generate markdown report
generate_markdown(results, 'output.md', filters, total_books)
```

### Working with the Database Module

```python
from calibre_search.db import create_readonly_copy, cleanup_readonly_copy

# Create a readonly copy for safe access
readonly_db = create_readonly_copy('metadata.db', 'metadata.db.readonly')

try:
    # Perform operations on readonly_db
    pass
finally:
    # Clean up
    cleanup_readonly_copy(readonly_db)
```

### Using the Query Builder

```python
from calibre_search.query import QueryBuilder

filters = {'title': 'Python', 'format': 'PDF'}
builder = QueryBuilder(filters)
query, params = builder.build()
```

### Generating Reports

```python
from calibre_search.report import MarkdownReportGenerator

results = [
    ('Learning Python', 'Mark Lutz', 'PDF, EPUB'),
    ('Programming Python', 'Mark Lutz', 'PDF')
]

filters = {'author': 'Lutz'}
total_books = 100

generator = MarkdownReportGenerator(results, filters, total_books)
generator.generate('catalog.md')
```

## Project Structure

```
calibre_report/
├── calibre_search/           # Main package
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command-line interface
│   ├── db.py                # Database operations
│   ├── query.py             # SQL query building
│   └── report.py            # Markdown report generation
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_db.py
│   ├── test_query.py
│   └── test_report.py
├── calibre_search.py         # Original monolithic script (deprecated)
├── setup.py                  # Package installation configuration
├── requirements.txt          # Package dependencies
└── README.md                 # This file
```

## Running Tests

Run all tests:

```bash
python -m unittest discover tests
```

Run specific test module:

```bash
python -m unittest tests.test_query
```

Run with verbose output:

```bash
python -m unittest discover tests -v
```

## Output Format

The tool generates a markdown file with the following sections:

1. **Header**: Title and generation timestamp
2. **Search Filters**: Applied filters (if any)
3. **Statistics**: Total books and matching books count
4. **Books Table**: Results in a formatted markdown table

Example output:

```markdown
# Calibre eBook Catalog

Generated: 2025-12-06 10:30:00

## Search Filters

- **Author**: Mark Lutz

## Statistics

- Total books in database: 150
- Books matching filters: 5

## Books

| Title | Author | Formats |
|-------|--------|----------|
| Learning Python | Mark Lutz | PDF, EPUB |
| Programming Python | Mark Lutz | PDF |
```

## Safety Features

- Creates readonly copy of database by default to prevent accidental modifications
- Automatic cleanup of temporary readonly copies
- Uses readonly connection mode for database access
- Comprehensive error handling

## Development

### Code Organization

The codebase follows a modular architecture:

- **db.py**: Database connection and operations
- **query.py**: SQL query construction with builder pattern
- **report.py**: Markdown report generation
- **cli.py**: Command-line interface and argument parsing

### Adding New Features

To add a new search filter:

1. Update `QueryBuilder` in [query.py](calibre_search/query.py)
2. Add filter method following the `_add_*_filter` pattern
3. Update `build()` method to call your new filter
4. Add corresponding CLI argument in [cli.py](calibre_search/cli.py)
5. Add tests in [tests/test_query.py](tests/test_query.py)

## License

This project is provided as-is for searching and cataloging Calibre ebook libraries.

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass
2. New features include tests
3. Code follows existing style
4. Documentation is updated

## Troubleshooting

### Database not found

Ensure the Calibre metadata.db path is correct. Default location is `~/Calibre/metadata.db`.

```bash
# Specify custom path
python -m calibre_search.cli --database /path/to/metadata.db
```

### Permission errors

If you encounter permission errors with readonly copy creation, use the `--no-copy` flag:

```bash
python -m calibre_search.cli --no-copy
```

### No results found

- Check that your search terms are spelled correctly
- Remember that searches are case-insensitive and use partial matching
- Try broader search terms

## Acknowledgments

This tool works with [Calibre](https://calibre-ebook.com/), the excellent ebook management software.

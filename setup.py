"""Setup configuration for calibre_search package."""

from setuptools import setup, find_packages
import os

# Read the README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='calibre-search',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Search Calibre metadata databases and generate markdown catalogs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/calibre-search',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='calibre ebook search catalog markdown',
    python_requires='>=3.6',
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        'console_scripts': [
            'calibre-search=calibre_search.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
)

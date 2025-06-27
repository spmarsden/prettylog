from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read().strip()

# Set the version number.
__version__ = '1.1.0'
with open('prettylog/_version.py', 'w', encoding='utf-8') as f:
    f.write(f"__version__ = '{__version__}'\n")

setup(
    name                          = 'prettylog',
    version                       = __version__,
    author                        = 'Stephen P Marsden',
    author_email                  = 'stephenpmarsden@gmail.com',
    description                   = 'Logging configuration and tools',
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/spmarsden/prettylog',
    packages                      = [
        'prettylog'
    ],
    entry_points                  = {
        'console_scripts': [
            'prettylog-example=prettylog.example:main',
        ],
    },
    python_requires               = '>=3.6',
    install_requires              = [
        'colorama',
        'tabulate'
    ],
)

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read().strip()

with open('version.txt', 'r', encoding='utf-8') as fh:
    version = fh.read().strip()

setup(
    name                          = 'prettylog',
    version                       = version,
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
            'prettylog-example=prettylog.scripts.example:main',
        ],
    },
    python_requires               = '>=3.6',
    install_requires              = [
        'colorama',
        'tabulate'
    ],
)

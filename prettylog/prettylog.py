import os
import logging
import colorama
from pathlib import Path
from typing import Callable, List, Any, Optional
from tabulate import tabulate

TABLE_FORMAT = 'simple_outline'

def print_table(*args, stream:Callable=print, tablefmt:str=TABLE_FORMAT, **kwargs) -> None:
        """
        Print a table using tabulate to the given stream.

        Args:
            *args: Positional arguments to pass to tabulate.
            stream (Callable): The stream to print to. Default is print.
            **kwargs: Keyword arguments to pass to tabulate
        """

        for line in tabulate(*args, **kwargs, tablefmt=tablefmt).split('\n'):
            stream(line)

        return

class ContinuousTable:
    def __init__(self, col_widths:List[int], col_align:List[str], stream:Callable=print):
        """
        Initialize a continuous table with the specified column widths and headers.
        """

        # Check that the column widths are valid.
        if not isinstance(col_widths, list) or not all(isinstance(w, int) and w > 0 for w in col_widths):
            raise ValueError("col_widths must be a list of positive integers")
        
        # Check that the column alignments are valid.
        if not all([c in ['<', '>', '^'] for c in col_align]):
            raise ValueError("col_align must be a list of < (left), > (right), or ^ (centre)")
        
        # Check that the column widths and alignments are the same length.
        if len(col_widths) != len(col_align):
            raise ValueError("col_widths and col_align must have the same length")

        self.col_widths = col_widths
        self.col_align = col_align
        self.stream = stream

    def start(self) -> None:
        """
        Start the continuous table by printing the top bar.
        """
        table_start = '┌─'
        for width in self.col_widths[:-1]:
            table_start += '─' * width + '─┬─'
        table_start += '─' * self.col_widths[-1] + '─┐'
        
        self.stream(table_start)
        
    def end(self) -> None:
        """
        End the continuous table by printing the bottom bar.
        """
        table_end = '└─'
        for width in self.col_widths[:-1]:
            table_end += '─' * width + '─┴─'
        table_end += '─' * self.col_widths[-1] + '─┘'
        
        self.stream(table_end)

    def hr(self) -> None:
        """
        Print a horizontal rule in the continuous table.
        """
        hr = '├─'
        for width in self.col_widths[:-1]:
            hr += '─' * width + '─┼─'
        hr += '─' * self.col_widths[-1] + '─┤'
        
        self.stream(hr)

    def row(self, line:List[Any], col_align=None, stream:Optional[Callable]=None) -> None:
        """
        Print a row in the continuous table with the specified line.
        """

        # If no stream is specified, use the default.
        if stream is None:
            stream = self.stream
        
        # If no column alignment is specified, use the default.
        if col_align is None:
            col_align = self.col_align
        
        row = '│ '
        for i, item in enumerate(line):
            row += f"{str(item):{col_align[i]}{self.col_widths[i]}} │ "
        
        stream(row)

def get_cache_dir() -> Path:
    """
    Get the cache directory for the current user.
    """

    # Define the default cache directory.
    cache_dir = Path(os.path.expanduser('~'), '.cache')

    # Check if the XDG_CACHE_HOME environment variable is set.
    if 'XDG_CACHE_HOME' in os.environ:
        cache_dir = Path(os.path.join(os.environ['XDG_CACHE_HOME']))

    return cache_dir

class CustomFormatter(logging.Formatter):

    def __init__(self, colour: bool=True, threaded: bool=False, verbose: bool=False):
        """
        A custom logging formatter that allows for coloured output, thread
        names, and verbose output.

        Args:
            colour   (bool): Whether to use colours in the log output.
            threaded (bool): Whether to include the thread name in the log
                output.
            verbose  (bool): Whether to include the file name and line number in
                the log output
        """

        # Validate the input arguments and store them as attributes.
        self._colour = bool(colour)
        self._threaded = bool(threaded)
        self._verbose = bool(verbose)

        # Define colours for different log levels.
        self.colours = {
            logging.DEBUG:    colorama.Fore.LIGHTBLACK_EX,
            logging.INFO:     colorama.Fore.RESET,
            logging.WARNING:  colorama.Fore.YELLOW,
            logging.ERROR:    colorama.Fore.RED,
            logging.CRITICAL: colorama.Style.BRIGHT + colorama.Fore.RED,
            'reset':          colorama.Style.RESET_ALL
        }

        # Define black and white formats.
        self.formats = {
            logging.DEBUG:    '%(asctime)s ┆ %(levelname)-8s ┆ %(message)s',
            logging.INFO:     '%(asctime)s ┆ %(levelname)-8s ┆ %(message)s',
            logging.WARNING:  '%(asctime)s ┆ %(levelname)-8s ┆ %(message)s',
            logging.ERROR:    '%(asctime)s ┆ %(levelname)-8s ┆ %(message)s',
            logging.CRITICAL: '%(asctime)s ┆ %(levelname)-8s ┆ %(message)s',
        }
    
    def get_format(self, level: int) -> str:
        """
        Get the log format for the given log level, including colours,
        threading, and verbosity.

        Args:
            level (int): The log level for which to get the format.
        """

        # Get the black and white format for the given log level.
        format = self.formats.get(level)
        
        # Ensure the log level is valid.
        if format is None:
            raise ValueError(f"Invalid log level: {level}")

        # Add thread name to the format if threaded is True.
        if self._threaded:
            format = format.replace('%(levelname)-8s', '%(levelname)-8s | %(threadName)s')

        # Add file name and line number to the format if verbose is True.
        if self._verbose:
            format = format.replace('%(message)s', '[%(name)s:%(lineno)d] %(message)s')

        # Add colours to the format if colourful is True.
        if self._colour:
            format = self.colours[level] + format + self.colours['reset']

        return format

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a string.

        Args:
            record (logging.LogRecord): The log record to format.
        """

        # Get the log format for the given log level.
        log_fmt = self.get_format(record.levelno)

        # Create a formatter object and return the formatted log message.
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)

def get_logging_config(log_file: Path, stream_log_level: int, colourful: bool=True):
    """
    Get the logging configuration dictionary. The configuration includes
    stream handlers for different log levels, as well as rotating file
    handlers for error, info, and debug messages.

    This should be called at the beginning of the program to configure the
    logging system.

    Note that log files will stream the full debug output, while the console
    will only display messages at the given log level or higher.

    Args:
        log_name (Path): The path to the log file. Suggestion: 
            "~/.cache/<package_name>/<module_name>/<module_name>.log"
        stream_log_level (int): The log level for the stream handler.
        colourful (bool): Whether to use colours in the log output.
    """

    # Ensure log_file is a Path object
    log_file = Path(log_file)

    # Create the log directory if it does not exist
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Initialize the list of handlers with the default stream handler
    package_handlers = ['default']
    
    # Get the string representation of the stream log level
    stream_log_level_str = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR:    "ERROR",
        logging.WARNING:  "WARNING",
        logging.INFO:     "INFO",
        logging.DEBUG:    "DEBUG"
    }[stream_log_level]

    package_handlers.extend([
            'error_rotating_file_handler',
            'info_rotating_file_handler',
            'debug_rotating_file_handler'
    ])

    # Choose the formatter based on the colourful flag
    default_formatter = 'colourful' if colourful else 'standard'
    
    # Return the logging configuration dictionary
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                '()': lambda: CustomFormatter(colour=False),
            },
            'colourful': {
                '()': CustomFormatter,
            },
            'log-file': {
                '()': lambda: CustomFormatter(colour=False, threaded=True, verbose=True),
            }
        },
        'handlers': {
            'default': {
                'level': stream_log_level_str,
                'formatter': default_formatter,
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
            'debug_rotating_file_handler': {
                'level': 'DEBUG',
                'formatter': 'log-file',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'mode': 'a',
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'info_rotating_file_handler': {
                'level': 'INFO',
                'formatter': 'log-file',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'mode': 'a',
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'error_rotating_file_handler': {
                'level': 'WARNING',
                'formatter': 'log-file',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'mode': 'a',
                'maxBytes': 1048576,
                'backupCount': 3
            }
        },
        'loggers': {
            '': {
                'level': logging.DEBUG,
                'handlers': package_handlers
            },
        }
    }

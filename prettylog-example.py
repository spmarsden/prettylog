import argparse
import prettylog
import time
import random

import logging.config

LOGGER = logging.getLogger(__name__)

def main() -> None:

    ## Command line arguments ##################################################

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Example script to demonstrate prettylog usage.')
    # Logging level.
    log_level_group = parser.add_mutually_exclusive_group(required=False)
    log_level_group.add_argument('-d', '--debug',    action='store_true', help='Set logging level to DEBUG.')
    log_level_group.add_argument('-i', '--info',     action='store_true', help='Set logging level to INFO (Default).')
    log_level_group.add_argument('-w', '--warning',  action='store_true', help='Set logging level to WARNING.')
    log_level_group.add_argument('-e', '--error',    action='store_true', help='Set logging level to ERROR.')
    log_level_group.add_argument('-c', '--critical', action='store_true', help='Set logging level to CRITICAL.')

    # Parse the arguments.
    args = parser.parse_args()

    # Logging level.
    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    elif args.warning:
        log_level = logging.WARNING
    elif args.error:
        log_level = logging.ERROR
    elif args.critical:
        log_level = logging.CRITICAL

    ## Set up logging ##########################################################

    # Set up logging.
    log_file = prettylog.get_cache_dir() / 'prettylog' / __name__ / f'{__name__}.log'
    logging.config.dictConfig(
        prettylog.get_logging_config(
            log_file = log_file,
            stream_log_level = log_level
        )
    )

    ## Welcome message #########################################################

    LOGGER.info('Welcome to the prettylog example script!')
    LOGGER.info(f'Log is also saved to: {log_file}')

    ## Show exmples of each logging level ######################################

    LOGGER.debug('This is a DEBUG message.')
    LOGGER.info('This is an INFO message.')
    LOGGER.warning('This is a WARNING message.')
    LOGGER.error('This is an ERROR message.')
    LOGGER.critical('This is a CRITICAL message.')

    ## Print a simple table ####################################################

    prettylog.print_table(
        headers=['Column 1', 'Column 2', 'Column 3'],
        rows=[
            ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3'],
            ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3'],
            ['Row 3, Col 1', 'Row 3, Col 2', 'Row 3, Col 3']
        ],
        stream = LOGGER.info
    )

    ## Print a continous table #################################################

    table = prettylog.ContinuousTable(
        col_widths = [20, 20],
        col_align  = ['>', '>'],
        stream     = LOGGER.info
    )
    # Print the opening line of the table.
    table.start()
    # Print the header row.
    table.row(['Row', 'Random Number'], col_align=['^', '^'])
    # Create a horizontal rule between the header and the data.
    table.hr()
    # Print some data rows.
    for i in range(10):
        # Simulate work being done.
        time.sleep(1)
        # Generate a random number.
        random_number = random.randint(1, 100)
        # Print the row with the random number.
        if i is 3:
            table.row([f'Row {i+1}', f'{random_number}'], stream = LOGGER.warning)
        else:
            table.row([f'Row {i+1}', f'{random_number}'])

if __name__ == "__main__":
    main()
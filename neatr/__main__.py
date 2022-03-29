#!/usr/bin/env python3

import argparse
import logging
import traceback
import sys
from pathlib import Path
from builtins import KeyboardInterrupt

from neatr.neat import neat


def main():
    processor = neat.Processor()

    try:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s - %(message)s',
            level=logging.INFO
        )

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-n',
            help='The Neat database',
            dest='database',
            default='/tmp/neatr/neat.db'
        )

        parser.add_argument(
            '-p',
            help='The extraction path',
            dest='path',
            default='/tmp/neatr'
        )

        parser.add_argument(
            '-d',
            help='Extract documents',
            dest='extract_documents',
            action='store_true'
        )

        parser.add_argument(
            '-r',
            help='Extract receipts',
            dest='extract_receipts',
            action='store_true'
        )

        parser.add_argument(
            '-D',
            help='Process documents',
            dest='process_documents',
            action='store_true'
        )

        parser.add_argument(
            '-R',
            help='Process receipts',
            dest='process_receipts',
            action='store_true'
        )

        arguments = parser.parse_args()
        processor.set_environment(neat.Environment.create(
            Path(arguments.database),
            Path(arguments.path)
        ))

        if arguments.extract_documents:
            processor.extract_documents()
        
        if arguments.process_documents:
            processor.process_documents()
        
        if arguments.extract_receipts:
            processor.extract_receipts()
        
        if arguments.process_receipts:
            processor.process_receipts()
        
    except KeyboardInterrupt:
        logging.debug('Exiting gracefully')
        sys.exit()
    except Exception as exception:
        logging.error(traceback.format_exc())

if __name__ == '__main__':
    main()

#!/usr/bin/python3

import time
import argparse
import logging
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import command

def main():
    try:
        utilities.save_cl_args()
        log_file, log_level = utilities.get_logging_config()
        if None not in (log_file, log_level):
            logging.basicConfig(filename=log_file, level=log_level)
        shared_dir = utilities.get_shared_directory()
        gram_handler = grammarhandler.GrammarHandler()
        gram_handler.load_grammars()
        logging.info('Started listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        previous_command = None
        while True:
            lines = utilities.get_buffer_lines(shared_dir)
            for line in lines:
                logging.info('Received input "{}" at {}'.format(line,
                    time.strftime("%Y-%m-%d %H:%M:%S")))
                current_command = command.Command(line.split(' '), previous_command)
                current_command.set_results(gram_handler)
                if not current_command.has_repeat_action():
                    previous_command = current_command
                current_command.do_results()
            time.sleep(.1)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        logging.info('Stopped listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    main()
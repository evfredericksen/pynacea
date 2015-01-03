#!/usr/bin/python3

import time
import argparse
import logging
import collections
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
        utilities.clear_directory(shared_dir)
        gram_handler = grammarhandler.GrammarHandler()
        gram_handler.load_grammars()
        logging.info('Started listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        command_history = collections.deque(maxlen=100)
        while True:
            lines = utilities.get_buffer_lines(shared_dir)
            for line in lines:
                logging.info('Received input "{}" at {}'.format(line,
                    time.strftime("%Y-%m-%d %H:%M:%S")))
                current_command = command.Command(line.split(' '), command_history)
                current_command.set_results(gram_handler)
                if not current_command.has_repeat_action():
                    command_history.append(current_command)
                current_command.do_results()
            time.sleep(.1)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        logging.info('Stopped listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    main()
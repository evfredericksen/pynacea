#!/usr/bin/python3

import time
import logging
import copy
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import command

def main():
    try:
        cl_arg_namespace = utilities.get_cl_args()
        utilities.save_cl_args(cl_arg_namespace)
        log_file, log_level = utilities.get_logging_config()
        if None not in (log_file, log_level):
            logging.basicConfig(filename=log_file, level=log_level)
        shared_dir = utilities.get_shared_directory()
        utilities.clear_directory(shared_dir)
        command_history = []
        gram_handler = grammarhandler.GrammarHandler()
        gram_handler.load_grammars(command_history)
        # bool that determines whether to run the main loop, checks
        # grammars._locals for patterns in SLEEP_PATTERNS and WAKE_UP_PATTERNS
        listening_status = True
        logging.info('Started listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        # main loop
        while True:
            if cl_arg_namespace.debug:
                lines = [input('> ')]
                time.sleep(cl_arg_namespace.debug_delay)
            else:
                lines = utilities.get_buffer_lines(shared_dir)
            for line in lines:
                updated_status = utilities.get_listening_status(listening_status, line)
                # go to next line if not currently listening or change in listening status
                if not listening_status or not updated_status:
                    listening_status = updated_status
                    continue
                logging.info('Received input "{}" at {}'.format(line,
                    time.strftime("%Y-%m-%d %H:%M:%S")))
                current_command = command.Command(line.split(' '), copy.copy(command_history))
                current_command.set_results(gram_handler)
                command_history.append(current_command)
                current_command.run()
            # Need to reset buffer
            if cl_arg_namespace.debug:
                input('\nPress Enter to Continue ')
            else:
                time.sleep(.1)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        logging.info('Stopped listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    main()
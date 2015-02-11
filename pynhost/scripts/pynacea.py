#!/usr/bin/python3

import time
import logging
import copy
import sys
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import command
from pynhost import configmenu
from pynhost import engineio

def main():
    try:
        cl_arg_namespace = utilities.get_cl_args()
        if cl_arg_namespace.config:
            configmenu.launch_config_menu()
            return
        engine_handler = engineio.get_engine_handler(cl_arg_namespace)
        log_file, log_level = utilities.get_logging_config()
        if None not in (log_file, log_level):
            logging.basicConfig(filename=log_file, level=log_level)
        command_history = []
        gram_handler = grammarhandler.GrammarHandler()
        gram_handler.load_grammars(command_history)
        # Dict for simulation of special modes
        mode_status = {'asleep': False, 'dictation mode': False, 'number mode': False}
        updated_status = mode_status
        logging.info('Started listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        # main loop
        while True:
            for line in engine_handler.get_lines():
                mode_status = updated_status
                updated_status, matched_pattern = utilities.get_new_status(mode_status, line)
                # go to next line if line matched mode status pattern or not currently awake
                if matched_pattern or updated_status['asleep']:
                    continue
                if mode_status['dictation mode']:
                    utilities.transcribe_line(line.split(), transcribe_mode=True)
                    continue
                if mode_status['number mode']:
                    utilities.transcribe_numbers(line)
                    continue
                logging.info('Received input "{}" at {}'.format(line,
                    time.strftime("%Y-%m-%d %H:%M:%S")))
                current_command = command.Command(line.split(' '),
                    copy.copy(command_history))
                current_command.set_results(gram_handler)
                command_history.append(current_command)
                current_command.run()
            time.sleep(.1)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        logging.info('Stopped listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    main()
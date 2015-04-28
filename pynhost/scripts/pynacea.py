#!/usr/bin/python3

import time
import logging
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import commands
from pynhost import configmenu
from pynhost import engineio
from pynhost import history
from pynhost import constants
from pynhost import api

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
        gram_handler = grammarhandler.GrammarHandler()
        print('Loading grammars...')
        gram_handler.load_grammars()
        # Dict for simulation of special modes
        mode_status = {'sleep mode': False, 'dictation mode': False, 'number mode': False, 'rule mode': False}
        updated_status = mode_status
        logging.info('Started listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        command_history = history.CommandHistory()
        print('Ready!')
        # main loop
        while True:
            for line in engine_handler.get_lines():
                mode_status = updated_status
                updated_status, matched_pattern = utilities.get_new_status(mode_status, line)
                # go to next line if line matched mode status pattern or not currently awake
                if matched_pattern or updated_status['sleep mode']:
                    continue
                if mode_status['dictation mode']:
                    api.send_string(line)
                    continue
                if mode_status['number mode']:
                    api.send_string(utilities.get_number_string(line))
                    continue
                logging.info('Received input "{}" at {}'.format(line,
                    time.strftime("%Y-%m-%d %H:%M:%S")))
                current_command = commands.Command(line.split(' '))
                current_command.set_results(gram_handler, mode_status['rule mode'])
                command_history.run_command(current_command, cl_arg_namespace.split_dictation)
            time.sleep(constants.MAIN_LOOP_DELAY)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        logging.info('Stopped listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    main()

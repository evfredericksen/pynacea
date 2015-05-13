#!/usr/bin/python3

import time
import logging
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import commands
from pynhost import config
from pynhost import engineio
from pynhost import history
from pynhost import constants
from pynhost import api

def main():
    try:
        cl_arg_namespace = utilities.get_cl_args()
        log_handler = utilities.create_logging_handler(cl_arg_namespace.verbal_feedback)
        engine_handler = engineio.get_engine_handler(cl_arg_namespace)
        gram_handler = grammarhandler.GrammarHandler()
        print('Loading grammars...')
        gram_handler.load_grammars()
        # Dict for simulation of special modes
        mode_status = {'sleep mode': False, 'dictation mode': False, 'number mode': False, 'rule mode': False}
        updated_status = mode_status
        utilities.log_message(log_handler, 'info', 'Started listening for input')
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
                utilities.log_message(log_handler, 'info', 'Received input "{}"'.format(line))
                current_command = commands.Command(line.split(' '))
                current_command.set_results(gram_handler, mode_status['rule mode'], log_handler)
                command_history.run_command(current_command)
            time.sleep(constants.MAIN_LOOP_DELAY)
    except Exception as e:
        utilities.log_message(log_handler, 'exception', e)
        raise e
    finally:
        utilities.log_message(log_handler, 'info', 'Stopped listening for input')

if __name__ == '__main__':
    main()

#!/usr/bin/python3

import time
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import commands
from pynhost import config
from pynhost import engineio
from pynhost import history
from pynhost import constants

def main():
    try:
        cl_arg_namespace = utilities.get_cl_args()
        log_handler = utilities.create_logging_handler(cl_arg_namespace.verbal_feedback)
        engine_handler = engineio.get_engine_handler(cl_arg_namespace)
        gram_handler = grammarhandler.GrammarHandler()
        print('Loading grammars...')
        gram_handler.load_grammars()
        utilities.log_message(log_handler, 'info', 'Started listening for input')
        command_history = history.CommandHistory()
        print('Ready!')
        # main loop
        while True:
            for line in engine_handler.get_lines():
                utilities.log_message(log_handler, 'info', 'Received input "{}"'.format(line))
                current_command = commands.Command(line.split(' '))
                try:
                    current_command.set_results(gram_handler, log_handler)
                    command_history.run_command(current_command)
                except Exception as e:
                    if cl_arg_namespace.permissive_mode:
                        utilities.log_message(log_handler, 'exception', e)
                    else:
                        raise e
            time.sleep(constants.MAIN_LOOP_DELAY)
    except Exception as e:
        utilities.log_message(log_handler, 'exception', e)
        raise e
    finally:
        utilities.log_message(log_handler, 'info', 'Stopped listening for input')

if __name__ == '__main__':
    main()

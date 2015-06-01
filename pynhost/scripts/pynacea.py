#!/usr/bin/python3

import time
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import commands
from pynhost import config
from pynhost import engineio
from pynhost import history
from pynhost import constants
from pynhost.platforms import platformhandler

def main():
    try:
        cl_arg_namespace = utilities.get_cl_args()
        log_handler = utilities.create_logging_handler(cl_arg_namespace.verbose,
            config.settings['logging directory'])
        if cl_arg_namespace.debug:
            engine = engineio.DebugEngine(cl_arg_namespace.debug_delay)
        else:
            engine = config.settings['engine']
        gram_handler = grammarhandler.GrammarHandler()
        print('Loading grammars...')
        gram_handler.load_grammars()
        utilities.log_message(log_handler, 'info', 'Started listening for input')
        command_history = history.CommandHistory()
        print('Ready!')
        # main loop
        while True:
            for line in engine.get_lines():
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
                platformhandler.flush_io_buffer()
            time.sleep(constants.MAIN_LOOP_DELAY)
    except Exception as e:
        utilities.log_message(log_handler, 'exception', e)
        raise e
    finally:
        engine.cleanup()
        utilities.log_message(log_handler, 'info', 'Stopped listening for input')

if __name__ == '__main__':
    main()

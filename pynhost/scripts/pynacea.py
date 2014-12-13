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
                c = command.Command(line.split(' '), previous_command)
                previous_command = c
                while c.remaining_words:
                    rule = c.get_matching_rule(gram_handler)
                    if rule is not None:
                        logging.info('Input "{}" matched rule "{}" in {}'.format(
                            ' '.join(rule.matching_words), rule.raw_text, rule.grammar))
                        c.results.append(rule)
                        c.execute_rule(rule)
                    else:
                        utilities.transcribe_line(list(c.remaining_words[0]),
                            len(c.remaining_words) != 1)
                        logging.debug('Transcribed word "{}"'.format(c.remaining_words[0]))
                        c.results.append(c.remaining_words[0])
                        c.remaining_words = c.remaining_words[1:]
            time.sleep(.1)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        logging.info('Stopped listening at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    main()
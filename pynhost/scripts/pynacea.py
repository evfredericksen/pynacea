#!/usr/bin/python3
import time
import sys
import os
from pkg_resources import Requirement, resource_filename
from pynhost import utilities
from pynhost import grammarhandler

CONFIG_PATH = resource_filename(Requirement.parse("pynhost"), "pynhost_config.ini")

def main():
    try:
        shared_dir = utilities.get_shared_directory(CONFIG_PATH)
    except:
        with open(CONFIG_PATH, 'w') as f:
            f.write('[settings]\n')
            f.write('shared_dir = None')
        shared_dir = 'None'
    if (shared_dir == 'None' or 
    len(sys.argv) == 2 and sys.argv[1] == 'config'):
        if shared_dir == 'None':
            print('Shared directory is currently not set')
        else:
            print('Shared directory is currently {}'.format(shared_dir))
        shared_dir = input('Enter the shared directory between the host '
        "operating system and the virtual machine (press 'q' to quit): ")
        if shared_dir != 'q':
            utilities.save_directory(CONFIG_PATH, shared_dir)
            print('Directory {} successfully saved!'.format(shared_dir))
    else:
        g = grammarhandler.GrammarHandler()
        g.load_grammars()
        last_action = []
        add_space = False
        while True:
            lines = utilities.get_buffer_lines(os.path.join(shared_dir, 'buffer.txt'))
            time.sleep(.2)
            for line in lines:
                result = {'remaining words': line.split(' ')}
                results = []
                last_action = []
                while result['remaining words']:
                    remaining_placeholder = result['remaining words']
                    result = g.get_matching_rule(result['remaining words'])
                    if result['rule'] is not None:
                        print(result)
                        result['rule'].func(result['new words'])
                        last_action.append((result['rule'].func, result['new words']))
                    else:
                        utilities.transcribe_line(list(remaining_placeholder[0]),
                            len(remaining_placeholder) != 1)
                        last_action.append(remaining_placeholder[0])
                        result['remaining words'] = remaining_placeholder[1:]

if __name__ == '__main__':
    main()

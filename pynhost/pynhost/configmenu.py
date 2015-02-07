import sys
from pynhost import utilities

def launch_config_menu():
    choice_string = "Choose an option ('q' to quit): "
    menu_choice = ''
    while menu_choice != 'q':
        print_main_menu()
        menu_choice = input(choice_string)
        if menu_choice == '1':
            handle_engine_change_menu()
        elif menu_choice == '2':
            handle_engine_settings_menu()
        elif menu_choice == '3':
            handle_logging_settings_menu()
        elif menu_choice != 'q':
            print('Invalid Input')
        print()

def make_choice(change_object, config_title, config_name):
    print('\n{} currently set to {}'.format(change_object, utilities.get_config_setting(config_title, config_name)))
    choice_input = input("Enter new {} or 'b' to go back: ".format(change_object))
    if choice_input != 'b':
        utilities.save_config_setting(config_title, config_name, choice_input)
        print('{} set to {}'.format(change_object, choice_input))
    print()

def print_main_menu():
    main_options = [
        'Change Speech To Text Engine',
        'Change Engine Settings',
        'Change Logging Settings',
    ]
    for i, option in enumerate(main_options, start=1):
        print('{}. {}'.format(i, option))

def handle_engine_change_menu():
    print()
    options = {
        'General/Shared Directory': 'shared_dir',
        'Sphinx': 'sphinx',
    }
    option_list = list(sorted(options))
    menu_choice = ''
    while menu_choice != 'b':
        current_engine = utilities.get_config_setting('local', 'input_format')
        for i, option in enumerate(option_list, start=1):
            prt_option = '{}. {}'.format(i, option)
            if options[option] == current_engine:
                prt_option += ' (current)'
            print(prt_option)
        menu_choice = input("Select an engine/input format ('b' to go back): ")
        if menu_choice == 'b':
            return
        if not menu_choice.isdigit() or int(menu_choice) not in range(1, len(options) + 1):
            print('Invalid Input\n')
        else:
            utilities.save_config_setting('local', 'input_format', options[option_list[int(menu_choice) - 1]])
            print('Engine set to {}\n'.format(option_list[int(menu_choice) - 1]))

def handle_engine_settings_menu():
    print()
    menu_choice = ''
    while menu_choice != 'b':
        print('1. Change Hidden Markov Models directory')
        print('2. Change Language Model filename')
        print('3. Change Dictionary')
        menu_choice = input("Choose an option ('b' to go back): ")
        if menu_choice == '1':
            make_choice('Hidden Mark Models directory', 'sphinx', 'hmm_directory')
        elif menu_choice == '2':
            make_choice('Language Model filename', 'sphinx', 'lm_filename')
        elif menu_choice == '3':
            make_choice('Dictionary', 'sphinx', 'dictionary')
        elif menu_choice != 'b':
            print('Invalid Choice\n')

def handle_logging_settings_menu():
    print()
    menu_choice = ''
    while menu_choice != 'b':
        print('1. Change logging level')
        print('2. Change logging filename')
        menu_choice = input("Choose an option ('b' to go back): ")
        if menu_choice == '1':
            make_choice('logging level', 'logging', 'logging_level')
        elif menu_choice == '2':
            make_choice('logging filename', 'logging', 'logging_file')
        elif menu_choice != 'b':
            print('Invalid Choice')
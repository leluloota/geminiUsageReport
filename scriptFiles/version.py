import socket
import platform
import os

hostName = 'Hostname: ' + socket.gethostname()
operating_system = 'OS: ' + platform.system()
osVersion = 'OS Version: ' + platform.release()
pythonVersion = 'Python version: ' + platform.python_version()
currentDirectory = 'Current path: ' + os.getcwd()


def version(info_log, program_name, program_version, log_file_name, version_publish_date, execution_mode):
    # Add printed values to list.
    # To list more details, just add them to the list. Out put is automatically populated.
    to_be_printed = ['VERSION DETAILS', 'Program name: ' + program_name, 'Program version: ' + program_version,
                     'Published: ' + version_publish_date, hostName, pythonVersion, operating_system, osVersion,
                     currentDirectory, 'Log file: ' + log_file_name, '', 'Execution mode: ' + execution_mode]
    star_count = len(max(to_be_printed, key=len)) + 3
    if star_count % 2:
        star_count += 1
    first = to_be_printed[0]
    del to_be_printed[0]
    top_row_start_count = ((star_count - len(first)) / 2) - 1
    count = 0
    first_row_stars = ''
    while count <= top_row_start_count:
        first_row_stars = first_row_stars + '*'
        count += 1
    lead = '* '
    top_row = first_row_stars + ' ' + first + ' ' + first_row_stars
    bottom_row = ''
    count = 0
    # Generate top and end rows
    while count <= star_count:
        bottom_row = bottom_row + '*'
        count += 1
    info_log(f'{top_row}')
    # Print entries
    for entry in to_be_printed:
        entry = lead + entry
        space_count = star_count - len(entry)
        count = 0
        while count < space_count:
            entry = entry + ' '
            count += 1
        entry = entry + '*'
        info_log(entry)
    info_log(f'{bottom_row}')


def operation_selections(info_log, selected_operations, execution_mode):
    selected_operations.insert(0, 'SELECTED OPERATIONS')
    star_count = len(max(selected_operations, key=len)) + 5
    if star_count % 2:
        star_count += 1
    first = selected_operations[0]
    del selected_operations[0]
    if not selected_operations:
        info_log('No operations selected')
        exit()
    else:
        top_row_start_count = ((star_count - len(first)) / 2) - 1
        count = 0
        first_row_stars = ''
        while count <= top_row_start_count:
            first_row_stars = first_row_stars + '*'
            count += 1
        lead = '* '
        top_row = first_row_stars + ' ' + first + ' ' + first_row_stars
        bottom_row = ''
        count = 0
        # Generate top and end rows
        while count <= star_count:
            bottom_row = bottom_row + '*'
            count += 1
        info_log(f'{top_row}')
        # Print entries
        for entry in selected_operations:
            operation = entry.split(':')[0]
            # info_log(operation)
            entry = lead + entry.split(':')[0] + ': ' + entry.split(':')[1]
            space_count = star_count - len(entry)
            count = 0
            while count < space_count:
                entry = entry + ' '
                count += 1
            entry = entry + '*'
            info_log(entry)
        info_log(f'{bottom_row}')

        if execution_mode == 'TEST':
            # Ask to continue
            user_input = input("Do You Want To Continue? [y/n]")
            if user_input.upper() == 'Y':
                info_log(f'Starting process...')
                info_log(f'')
            else:
                info_log(f'Process cancelled')
                exit()
        else:
            info_log('')

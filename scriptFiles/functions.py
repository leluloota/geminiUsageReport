# Import modules
from datetime import datetime
import re

process_time = datetime.now().strftime("%H:%M:%S")
process_date = datetime.now().strftime("%Y-%m-%d")


def parser(source_log_file, work_path, info_log, error_log, debug_log):
    info_log(f'Parsing data from: {work_path}{source_log_file}')
    info_log('')
    login_success_count = 0
    login_error_count = 0
    logout_success_count = 0
    logout_error_count = 0
    skipped_count = 0
    login_user_count = 0
    logout_user_count = 0
    login_odbc_count = 0
    logout_odbc_count = 0
    login_batch_count = 0
    logout_batch_count = 0
    login_backup_count = 0
    logout_backup_count = 0
    # Search ABL loging rows and parse data
    with (open(work_path + source_log_file) as login_data):
        for line_number, line in enumerate(login_data):
            debug_log(f'Row data: {line}')
            if 'Login' in line:
                login_data = {'Login process date time:': str(process_date + ' ' + datetime.now().strftime("%H:%M:%S"))}
                login_line_number = line_number
                # debug_log(line)
                debug_log(f'Login row found, row numer: {login_line_number + 1}')
                if 'userid' in line and 'client type ABL' in line:  # Login type User handling
                    login_type = 'USER'
                    login_user_count += 1
                    login_data.update({'Login type:': login_type})
                    try:
                        # Get login date
                        login_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                        debug_log(f'login_date = {login_date}')
                        debug_log(f'login_date = {login_date}')
                        # Get login time
                        login_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                        debug_log(f'login_time = {login_time}')
                        # Get login PID
                        login_pid = line[31:44].strip()
                        debug_log(f'login_pid = {login_pid}')
                        # Get login host name
                        start = str(re.escape(' , on '))  # Start string for regexp
                        end = str(re.escape(' using'))  # End string for regexp
                        login_host_name = re.findall(start + "(.*)" + end, line)[0]
                        debug_log(f'login_host_name = {login_host_name}')
                        # Get login user number
                        start = str(re.escape('Login usernum '))  # Start string for regexp
                        end = str(re.escape(', userid'))  # End string for regexp
                        login_user_number = re.findall(start + "(.*)" + end, line)[0]
                        debug_log(f'User number: {login_user_number}')
                        login_success_count += 1
                        login_data.update({'Login type:': login_type,
                                           'Login date time:': login_date + ' ' + login_time,
                                           'Login PID:': login_pid,
                                           'Login host name:': login_host_name,
                                           'Login user number:': login_user_number})
                    except IndexError as e:
                        error_log(f'Error while extracting login row data. Row number: {login_line_number}')
                        error_log(f'Error message:\n'
                                  f'{e}')
                        login_error_count += 1
                elif 'remote SQL client' in line or 'SQLSRV2' in line:  # Login type SQL client handling
                    login_type = 'ODBC'
                    login_data.update({'Login type:': login_type})
                    login_odbc_count += 1
                    debug_log(f'Login type: {login_type}')
                    # Get login date
                    login_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                    debug_log(f'login_date = {login_date}')
                    # Get login time
                    login_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                    debug_log(f'login_time = {login_time}')
                    # Get login PID
                    login_pid = line[31:44].strip()
                    debug_log(f'login_pid = {login_pid}')
                    login_success_count += 1
                    login_data.update({'Login type:': login_type,
                                       'Login date time:': login_date + ' ' + login_time,
                                       'Login PID:': login_pid})
                elif 'by SYSTEM' in line:  # Login type SYSTEM client handling
                    if 'ABL' in line or 'on batch' in line:  # Batch user
                        login_type = 'BATCH'
                        login_data.update({'Login type:': login_type})
                        login_batch_count += 1
                    elif 'BACKUP' in line:  # Database backup
                        login_type = 'BACKUP'
                        login_data.update({'Login type:': login_type})
                        login_backup_count += 1
                    # Get login date
                    login_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                    debug_log(f'login_date = {login_date}')
                    # Get login time
                    login_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                    debug_log(f'login_time = {login_time}')
                    # Get login PID
                    login_pid = line[31:44].strip()
                    debug_log(f'login_pid = {login_pid}')
                    login_success_count += 1
                    login_data.update({'Login type:': login_type,
                                       'Login date time:': login_date + ' ' + login_time,
                                       'Login PID:': login_pid})
                else:
                    login_error_count += 1
                    error_log('')
                    error_log(f'Error while parsing login row data. Row number: {logout_line_number + 1}')
                    error_log('')
                info_log(f'Write login data to database')
                parsed_data = ''
                for key, value in login_data.items():
                    parsed_data = parsed_data + key + ' ' + value + '\n'
                info_log(parsed_data)
                info_log('')

            # Search Logout row for user
            elif 'Logout' in line:
                logout_line_number = line_number
                # debug_log(line)
                debug_log(f'Logout row found: {logout_line_number + 1}')
                logout_data = {'Logout process date time:': str(
                    process_date + ' ' + datetime.now().strftime("%H:%M:%S"))}
                if 'usernum' in line:
                    logout_type = 'USER'
                    logout_user_count += 1
                    debug_log(f'Logout type: {logout_type}')
                    try:
                        # Get logout date
                        logout_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                        debug_log(f'logout_date = {logout_date}')
                        # Get logout time
                        logout_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                        debug_log(f'logout_time = {logout_time}')
                        # Get logout PID
                        logout_pid = line[31:44].strip()
                        debug_log(f'logout_pid = {logout_pid}')
                        # Get logout host name
                        start = str(re.escape('on '))  # Start string for regexp
                        end = str(re.escape('.'))  # End string for regexp
                        logout_host_name = re.findall(start + "(.*)" + end, line)[0]
                        debug_log(f'logout_host_name: {logout_host_name}')
                        # Get logout user number
                        start = str(re.escape('Logout usernum '))  # Start string for regexp
                        end = str(re.escape(', userid'))  # End string for regexp
                        logout_user_number = re.findall(start + "(.*)" + end, line)[0]
                        debug_log(f'User number: {logout_user_number}')
                        logout_success_count += 1
                        logout_data.update({'Logout type:': logout_type,
                                            'Logout date time:': logout_date + ' ' + logout_time,
                                            'Logout PID:': logout_pid,
                                            'Logout host name:': logout_host_name,
                                            'Logout user number:': logout_user_number})
                    except IndexError as e:
                        error_log(f'Error while extracting logout row data. Row number: {logout_line_number + 1}')
                        error_log(f'Error message:\n'
                                  f'e=e'.format(e=e))
                        logout_error_count += 1
                elif 'by batch' in line or 'on batch' in line:
                    logout_type = 'BATCH'
                    logout_batch_count += 1
                    debug_log(f'Logout type: {logout_type}')
                    # Get logout date
                    logout_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                    debug_log(f'logout_date = {logout_date}')
                    # Get logout time
                    logout_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                    debug_log(f'logout_time = {logout_time}')
                    # Get logout PID
                    logout_pid = line[31:44].strip()
                    debug_log(f'logout_pid = {logout_pid}')
                    logout_success_count += 1
                    logout_data.update({'Logout type:': logout_type,
                                        'Logout date time:': logout_date + ' ' + logout_time,
                                        'Logout PID:': logout_pid})
                elif 'by SYSTEM' in line:
                    logout_type = 'BACKUP'
                    logout_backup_count += 1
                    debug_log(f'Logout type: {logout_type}')
                    # Get logout date
                    logout_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                    debug_log(f'logout_date = {logout_date}')
                    # Get logout time
                    logout_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                    debug_log(f'logout_time = {logout_time}')
                    # Get logout PID
                    logout_pid = line[31:44].strip()
                    debug_log(f'logout_pid = {logout_pid}')
                    logout_success_count += 1
                    logout_data.update({'Logout type:': logout_type,
                                        'Logout date time:': logout_date + ' ' + logout_time,
                                        'Logout PID:': logout_pid})
                elif 'SQLSRV2' in line or 'by odbc' in line:
                    logout_type = 'ODBC'
                    logout_odbc_count += 1
                    info_log(f'Logout type: {logout_type}')
                    # Get logout date
                    logout_date = str(datetime.strptime(line[1:11], format('%Y/%m/%d')).date())
                    debug_log(f'logout_date = {logout_date}')
                    # Get logout time
                    logout_time = str(datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S'))
                    debug_log(f'logout_time = {logout_time}')
                    # Get logout PID
                    logout_pid = line[31:44].strip()
                    debug_log(f'logout_pid = {logout_pid}')
                    logout_success_count += 1
                    logout_data.update({'Logout type:': logout_type,
                                        'Logout date time:': logout_date + ' ' + logout_time,
                                        'Logout PID:': logout_pid})
                else:
                    logout_error_count += 1
                    error_log('')
                    error_log(f'Error while parsing logout row data. Row number: {logout_line_number + 1}')
                    error_log('')
                info_log(f'Write logout data to database')
                parsed_data = ''
                for key, value in logout_data.items():
                    parsed_data = parsed_data + key + ' ' + value + '\n'
                info_log(parsed_data)
                info_log('')
            else:
                debug_log(f'Skipping line: {line_number}')
                skipped_count += 1
                debug_log('')
        info_log('')
        info_log(f'Result of parsing file: {work_path}{source_log_file}:\n'
                 f'Batch counts:\n'
                 f' Login: {login_batch_count}\n'
                 f' Logout: {logout_batch_count}\n'
                 f'User counts:\n'
                 f' Login: {login_user_count}\n'
                 f' Logout: {logout_user_count}\n'
                 f'ODBC counts:\n'
                 f' Login: {login_odbc_count}\n'
                 f' Logout: {logout_odbc_count}\n'
                 f'Backup counts:\n'
                 f' Login: {login_backup_count}\n'
                 f' Logout: {logout_backup_count}\n'
                 f'')
        info_log(f'***** SUCCESS COUNTS *****\n'
                 f'Login success count: {login_success_count}\n'
                 f'Logout success count: {logout_success_count}\n'
                 f'\n'
                 f'***** ERROR COUNTS *****\n'
                 f'Login error count: {login_error_count}\n'
                 f'Logout error count: {logout_error_count}\n'
                 f'\n'
                 f'***** OTHER COUNTS *****\n'
                 f'Rows skipped: {skipped_count}')

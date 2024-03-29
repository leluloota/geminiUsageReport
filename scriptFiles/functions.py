# Import modules
from datetime import datetime
import re


def parser(log_file, work_path, info_log, error_log, debug_log):
    info_log(f'Parsing data from: {work_path}{log_file}')
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
    with (open(work_path + log_file) as login_data):
        for line_number, line in enumerate(login_data):
            debug_log(f'Row data: {line}')
            if 'Login' in line:
                login_line_number = line_number
                # debug_log(line)
                info_log(f'Login row found, row numer: {login_line_number + 1}')
                if 'userid' in line and 'client type ABL' in line:  # Login type User handling
                    login_type = 'USER'
                    login_user_count += 1
                    info_log(f'Login type: {login_type}')
                    try:
                        # Get login date
                        login_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                        debug_log(f'login_date = {login_date}')
                        # Get login time
                        login_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')
                        debug_log(f'login_time = {login_time}')
                        # Get login PID
                        login_pid = line[31:44].strip()
                        debug_log(f'login_pid = {login_pid}')
                        # Get login host name
                        start = str(re.escape(' , on '))  # Start string for regexp
                        end = str(re.escape(' using'))  # End string for regexp
                        login_host_name = re.findall(start + "(.*)" + end, line)[0]
                        info_log(f'login_host_name = {login_host_name}')
                        # Get login user number
                        start = str(re.escape('Login usernum '))  # Start string for regexp
                        end = str(re.escape(', userid'))  # End string for regexp
                        login_user_number = re.findall(start + "(.*)" + end, line)[0]
                        debug_log(f'User number: {login_user_number}')
                        login_success_count += 1
                    except IndexError as e:
                        error_log(f'Error while extracting login row data. Row number: {login_line_number}')
                        error_log(f'Error message:\n'
                                  f'{e}')
                        login_error_count += 1
                elif 'remote SQL client' in line or 'SQLSRV2' in line:  # Login type SQL client handling
                    login_type = 'ODBC'
                    login_odbc_count += 1
                    debug_log(f'Login type: {login_type}')
                    # Get login date
                    login_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                    debug_log(f'login_date = {login_date}')
                    # Get login time
                    login_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')
                    debug_log(f'login_time = {login_time}')
                    # Get login PID
                    login_pid = line[31:44].strip()
                    debug_log(f'login_pid = {login_pid}')
                    login_success_count += 1
                elif 'by SYSTEM' in line:  # Login type SYSTEM client handling
                    if 'ABL' in line:  # Batch user
                        login_type = 'BATCH'
                        login_batch_count += 1
                        info_log(f'Login type: {login_type}')
                    elif 'BACKUP' in line:  # Database backup
                        login_type = 'BACKUP'
                        login_backup_count += 1
                        info_log(f'Login type: {login_type}')
                    # Get login date
                    login_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                    debug_log(f'login_date = {login_date}')
                    # Get login time
                    login_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')
                    debug_log(f'login_time = {login_time}')
                    # Get login PID
                    login_pid = line[31:44].strip()
                    debug_log(f'login_pid = {login_pid}')
                    login_success_count += 1
                else:
                    login_error_count += 1
                    error_log('')
                    error_log(f'Error while parsing login row data. Row number: {logout_line_number + 1}')
                    error_log('')
                info_log(f'Write login data to database')
                info_log('')

            # Search Logout row for user, iteration started from login row
            elif 'Logout' in line:
                logout_line_number = line_number
                # debug_log(line)
                info_log(f'Logout row found: {logout_line_number + 1}')
                if 'usernum' in line:
                    logout_type = 'USER'
                    logout_user_count += 1
                    info_log(f'Logout type: {logout_type}')
                    try:
                        # Get logout date
                        logout_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                        debug_log(f'logout_date = {logout_date}')
                        # Get logout time
                        logout_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')  #
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
                    except IndexError as e:
                        error_log(f'Error while extracting logout row data. Row number: {logout_line_number + 1}')
                        error_log(f'Error message:\n'
                                  f'e=e'.format(e=e))
                        logout_error_count += 1
                elif 'by batch' in line:
                    logout_type = 'BATCH'
                    logout_batch_count += 1
                    info_log(f'Logout type: {logout_type}')
                    # Get logout date
                    logout_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                    debug_log(f'logout_date = {logout_date}')
                    # Get logout time
                    logout_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')  #
                    debug_log(f'logout_time = {logout_time}')
                    # Get logout PID
                    logout_pid = line[31:44].strip()
                    debug_log(f'logout_pid = {logout_pid}')
                    logout_success_count += 1
                elif 'by SYSTEM' in line:
                    logout_type = 'BACKUP'
                    logout_backup_count += 1
                    debug_log(f'Logout type: {logout_type}')
                    # Get logout date
                    logout_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                    debug_log(f'logout_date = {logout_date}')
                    # Get logout time
                    logout_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')  #
                    debug_log(f'logout_time = {logout_time}')
                    # Get logout PID
                    logout_pid = line[31:44].strip()
                    debug_log(f'logout_pid = {logout_pid}')
                    logout_success_count += 1
                elif 'SQLSRV2' in line or 'by odbc' in line:
                    logout_type = 'ODBC'
                    logout_odbc_count += 1
                    info_log(f'Logout type: {logout_type}')
                    # Get logout date
                    logout_date = datetime.strptime(line[1:11], format('%Y/%m/%d')).date()
                    debug_log(f'logout_date = {logout_date}')
                    # Get logout time
                    logout_time = datetime.strptime(line[12:29], format('%H:%M:%S.%f%z')).strftime('%H:%M:%S')  #
                    debug_log(f'logout_time = {logout_time}')
                    # Get logout PID
                    logout_pid = line[31:44].strip()
                    debug_log(f'logout_pid = {logout_pid}')
                    logout_success_count += 1
                else:
                    logout_error_count += 1
                    error_log('')
                    error_log(f'Error while parsing logout row data. Row number: {logout_line_number + 1}')
                    error_log('')
                info_log(f'Write logout data to database')
                info_log('')
            else:
                debug_log(f'Skipping line: {line_number}')
                skipped_count += 1
                debug_log('')
        info_log('')
        info_log(f'Result of parsing file: {work_path}{log_file}:\n'
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

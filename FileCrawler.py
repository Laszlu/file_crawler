import os
from datetime import datetime
from pathlib import Path

backup_date_path = '/Users/laszloferreyra/Documents/backup_date.txt'
backup_log_path = '/Users/laszloferreyra/Documents/files_to_backup.txt'

base_path = Path('/Users/laszloferreyra')


def get_backup_date():
    with open(backup_date_path, 'r') as f:
        date = f.read()
        print(date)
        return date


def write_backup_date():
    with open(backup_date_path, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def print_intro(backup_date_str):
    backup_time = datetime.strptime(backup_date_str, '%Y-%m-%d %H:%M:%S')
    print('###############################################################################')
    print('FILE CHECKER STARTING')
    print('LAST BACKUP: ', backup_time)
    print('###############################################################################')


def check_files(backup_date_str, directory_path):
    backup_time = datetime.strptime(backup_date_str, '%Y-%m-%d %H:%M:%S')

    for root, dir_names, file_names in os.walk(directory_path):
        for file_name in file_names:
            try:
                if '.' in root or 'Library' in root or 'node_modules' in root:
                    continue
                if file_name == '.DS_Store':
                    continue
                modify_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file_name)))
                if modify_time > backup_time:
                    print('File: ', os.path.join(root, file_name))
                    print(modify_time)
                    print(backup_time)
                    print('File was modified after last backup')
                    with open(backup_log_path, 'a') as f:
                        f.write(os.path.join(root, file_name))
                        f.write('\n')
            except FileNotFoundError:
                print(os.path.join(root, file_name), 'not found!')
            finally:
                continue

        for dir_name in dir_names:
            dir_path = os.path.join(root, dir_name)
            if '.' in dir_path or 'node_modules' in dir_path:
                continue
            if (dir_name == 'Documents' or dir_name == 'Desktop' or dir_name == 'Downloads' or
                    dir_name == 'Pictures' or dir_name == 'Postman' or
                    dir_name == 'Projects' or dir_name == 'Public'):
                print('\n------------------------------------------------------------')
                # os.path.join(root, dir_name)
                print('directory: ', dir_name, '\n')
                print('Path: ', dir_path, '\n')
                check_files(backup_date_str, os.path.join(root, dir_name))


if __name__ == '__main__':
    backup_date = get_backup_date()
    print_intro(backup_date)
    check_files(backup_date, base_path)
    write_backup_date()


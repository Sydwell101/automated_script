from Device import *
import collections
import os

UserCredentials = collections.namedtuple('UserCredentials',
                                         'username, password')


def main():
    print_header()
    name = 'credentials'
    csv_file = 'newfile'

    # Add devices you want to configure/monitor on the devices-list.
    devices = []

    filename = 'lldp-info'

    for device in devices:
        device.connect_to_device(name)
        device.config_device(name)
        device.get_lldp_info(filename, name)
        device.get_lldp_ip_address(filename, name)
        device.get_ap_mac_address(filename)
        device.get_ap_mac_address_info(filename, name, csv_file)
        print('Done.' + '\n')


def get_username_password(name):
    filename = get_filename_full_path(name)

    if not os.path.exists(filename):
        print(f'File "{filename}" not found.')
    else:
        with open(filename) as fin:
            for entry in fin:
                if entry.find('username') != -1:
                    search_user = entry.strip()
                    break
            for l in fin:
                if l.find('password') != -1:
                    search_pass = l.strip()
                    break

    username = search_user.split(':')[1].strip()
    password = search_pass.split(':')[1].strip()

    user = UserCredentials(username=username, password=password)
    return user


def get_filename_full_path(name):
    filename = os.path.abspath(os.path.join('.', 'Files', name + '.txt'))
    return filename


def print_header():
    print('--------------------------')
    print('    NTP SERVER SCRIPT')
    print('--------------------------')
    print()


if __name__ == '__main__':
    main()

from Device import *
import collections
import os

UserCredentials = collections.namedtuple('UserCredentials',
                                         'username, password')


def main():
    print_header()
    name = 'credentials'
    csv_file = 'newfile'
    device1 = CiscoDevice('196.160.66.33')
    device1.connect_to_device(name)
    device1.config_device(name)

    filename = 'lldp-info'
    device1.get_lldp_info(filename, name)
    print()
    device1.get_lldp_ip_address(filename, name)
    device1.get_ap_mac_address(filename)
    device1.get_ap_mac_address_info(filename, name, csv_file)


def get_username_password(name):
    filename = get_filename_full_path(name)
    lines = list()
    username = None
    password = None

    if not os.path.exists(filename):
        print('File not found.')
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

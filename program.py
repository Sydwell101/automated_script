from Device import *
import collections
import os


UserCredentials = collections.namedtuple('UserCredentials',
                                         'username, password')


def main():
    print_header()
    name = 'credentials'
    device1 = CiscoDevice('196.160.66.33')
    device1.connect_to_device(name)
    device1.config_device(name)

    filename = 'lldp-info'
    device1.get_lldp_info(filename, name)
    print()
    device1.get_lldp_ip_address(filename, name)


def get_username_password(name):
    filename = get_filename_full_path(name)
    lines = list()

    if not os.path.exists(filename):
        print('File not found.')
    else:
        with open(filename) as fin:
            for entry in fin.readlines():
                entry = entry.strip()
                lines.append(entry)

    u_name = lines[0]
    p_word = lines[1]

    usern = u_name[17:31].strip()
    passw = p_word[10:-1].strip()

    user = UserCredentials(username=usern, password=passw)
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

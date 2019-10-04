from netmiko import ConnectHandler
import collections
import connect
import os

UserCredentials = collections.namedtuple('UserCredentials',
                                         'username, password')


def main():
    print('--------------------------')
    print('    NTP SERVER SCRIPT')
    print('--------------------------')
    name = 'System(s)'
    filename = 'lldp-info'
    # get_filename_full_path(name)
    # config_device(name)
    # connect.get_lldp_info(filename, name)
    connect.read_data(filename, name)
    # get_username_password(name)


def config_device(name):
    connect = connect_to_device(name)
    config_command = ''
    cmd = 'show run | include ntp server'
    ping = 'ping {}'.format(connect.host)

    ping_output = connect.send_command(ping)
    print(ping_output)

    print('Connecting to {}...'.format(connect.host))

    if connect:
        show_output = ''
        config_command = ['ntp server 196.26.5.10', 'ntp server 196.4.160.4']

        for config in config_command:
            output = connect.send_config_set(config)
            print(output)

        show_output = connect.send_command(cmd)
        print(show_output)

    else:
        print('Failed to send config "{}"'.format(config_command))


def connect_to_device(name):
    user = get_username_password(name)
    ar1 = {
        'device_type': 'cisco_ios',
        'ip': '196.160.66.33',
        'username': '{}'.format(user.username),
        'password': '{}'.format(user.password)
    }

    connect = ConnectHandler(**ar1)

    if not connect.is_alive():
        print('Connection refused.')
    else:
        return connect


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


if __name__ == '__main__':
    main()

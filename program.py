import collections
import connect
import os
import csv
import requests

UserCredentials = collections.namedtuple('UserCredentials',
                                         'username, password')


def main():
    print('--------------------------')
    print('    NTP SERVER SCRIPT')
    print('--------------------------')
    print()
    name = 'credentials'
    filename = 'lldp-info'
    file = 'newfile'
    # get_filename_full_path(name)
    # config_device(name)
    # connect.get_lldp_info(filename, name)
    # connect.read_data(filename, name)

    get_ap_port_info(filename, name, file)


def config_device(name):
    conn = connect.connect_to_device(name)
    config_command = ''
    cmd = 'show run | include ntp server'
    ping = 'ping {}'.format(conn.host)

    ping_output = conn.send_command(ping)
    print(ping_output)

    print('Connecting to {}...'.format(conn.host))

    if conn:
        show_output = ''
        config_command = ['ntp server 196.26.5.10', 'ntp server 196.4.160.4']

        for config in config_command:
            output = conn.send_config_set(config)
            print(output)

        show_output = conn.send_command(cmd)
        print(show_output)

    else:
        print('Failed to send config "{}"'.format(config_command))


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


def get_ap_port_info(fname, name, file):
    filename = os.path.abspath(os.path.join('.', 'Files', file + '.csv'))
    mac_address = connect.get_ap_mac_address(fname)
    conn = connect.connect_to_device(name)
    cmd = 'show mac-address-table address {}'.format(mac_address)

    try:
        if conn:
            out = conn.send_command(cmd)
            lines = out.split('\n')

            line = lines[2].split('\t')
            new_line = ''
            for l in line:
                if len(l) > 0:
                    l = l.strip('\t')
                    l = l.strip(' ')
                    new_line = new_line + l + ' '

        with open(filename, 'w') as fout:
            csv_writer = csv.writer(fout)
            new_line = new_line.split(' ')
            csv_writer.writerow(new_line)

    except ConnectionRefusedError:
        print('Connection refused')


if __name__ == '__main__':
    main()

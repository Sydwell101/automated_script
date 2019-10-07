from program import get_filename_full_path, get_username_password, get_ap_port_info
from netmiko import ConnectHandler
import os


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


def get_lldp_info(fname, name):
    connect = connect_to_device(name)
    print('Connecting to {}...'.format(connect.host))
    cmd = 'show lldp neighbors detail'
    # lines = list()
    filename = get_filename_full_path(fname)

    if connect:
        output = connect.send_command(cmd)
        output = output.strip()
        with open(filename, 'w') as fout:
            fout.write(output)

        print('Writing to {}...'.format(filename))
    else:
        print('Connection aborted')


def read_data(fname, name):
    filename = get_filename_full_path(fname)
    lines = list()
    con = connect_to_device(name)

    if os.path.exists(filename):
        with open(filename) as fin:
            for line in fin:
                lines.append(line.strip())

    ip = lines[14].split(':')

    cmd = 'ping {}'.format(ip[1].strip())
    output = con.send_command(cmd)
    print(output)


def get_ap_mac_address(filename):
    # url = 'https://196.160.9.15:7443/api/public'
    # send_request = requests.get(url)
    # print(send_request.status_code)
    filename = get_filename_full_path(filename)
    data = []

    if os.path.exists(filename):
        with open(filename) as fout:
            data = fout.readlines()

    chassis_id = data[2]
    mac_address = chassis_id.split(':')[1].strip()

    return mac_address

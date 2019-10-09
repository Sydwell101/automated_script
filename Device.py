import program
import sys
import os
import csv
from netmiko import ConnectHandler


class CiscoDevice:
    def __init__(self, host: str):
        self.host = host.strip()

    def connect_to_device(self, filename):
        user = program.get_username_password(filename)
        log = []
        fname = 'log.txt'

        ar1 = {
            'device_type': 'cisco_ios',
            'ip': f'{self.host}',
            'username': f'{user.username}',
            'password': f'{user.password}'
        }

        try:
            connect = ConnectHandler(**ar1)

            if connect.is_alive():
                return connect

        except ConnectionRefusedError:
            print('Connection refused.')
        except:
            log.append(sys.exc_info()[1])
            with open(fname, 'w') as fout:
                print(f'Will log error in {os.path.abspath(fname)}..')
                for error in log:
                    fout.write(str(error))

    def config_device(self, filename):
        conn = self.connect_to_device(filename)

        config_command = ''
        cmd = 'show run | include ntp server'
        ping = f'ping {conn.host}'

        ping_output = conn.send_command(ping)
        print(ping_output)

        if conn:
            config_command = ['ntp server 196.26.5.10', 'ntp server 196.4.160.4']

            for config in config_command:
                output = conn.send_config_set(config)
                print(output)

            show_output = conn.send_command(cmd)
            print()
            print('show run | inc ntp server:')
            print(show_output)

        else:
            print(f'Failed to send config "{config_command}"')

    def get_lldp_info(self, fname, name):
        connect = self.connect_to_device(name)
        cmd = 'show lldp neighbors detail'
        # lines = list()
        filename = program.get_filename_full_path(fname)

        if connect:
            output = connect.send_command(cmd)
            output = output.strip()
            with open(filename, 'w') as fout:
                print()
                print(f'LLDP data will be saved to {filename}..')
                fout.write(output)
        else:
            print('Connection closed.')

    def get_lldp_ip_address(self, fname, name):
        lines = list()
        con = self.connect_to_device(name)

        filename = program.get_filename_full_path(fname)

        if os.path.exists(filename):
            with open(filename) as fin:
                for line in fin:
                    lines.append(line.strip())

        ip = lines[14].split(':')

        cmd = 'ping {}'.format(ip[1].strip())
        output = con.send_command(cmd)
        print(output)

    def get_ap_mac_address(self, filename):
        # url = 'https://196.160.9.15:7443/api/public'
        # send_request = requests.get(url)
        # print(send_request.status_code)
        filename = program.get_filename_full_path(filename)
        data = []

        if os.path.exists(filename):
            with open(filename) as fout:
                data = fout.readlines()

        chassis_id = data[2]
        mac_address = chassis_id.split(':')[1].strip()

        return mac_address

    def get_ap_port_info(self, fname, name, file):
        filename = os.path.abspath(os.path.join('.', 'Files', file + '.csv'))
        mac_address = self.get_ap_mac_address(fname)
        conn = self.connect_to_device(name)
        cmd = 'show mac-address-table address {}'.format(mac_address)
        log = []

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
        except:
            log.append(sys.exc_info()[1])
            with open('log.txt', 'w') as fout:
                print(f'Will log error in {os.path.abspath(fname)}..')
                for error in log:
                    fout.write(str(error))

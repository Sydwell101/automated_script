import program
import os


def get_lldp_info(fname, name):
    connect = program.connect_to_device(name)
    print('Connecting to {}...'.format(connect.host))
    cmd = 'show lldp neighbors detail'
    # lines = list()
    filename = program.get_filename_full_path(fname)

    if connect:
        output = connect.send_command(cmd)
        output = output.strip()
        with open(filename, 'w') as fout:
            fout.write(output)

        print('Writing to {}...'.format(filename))
    else:
        print('Connection aborted')


def read_data(fname, name):
    filename = program.get_filename_full_path(fname)
    lines = list()
    con = program.connect_to_device(name)

    if os.path.exists(filename):
        with open(filename) as fin:
            for line in fin:
                lines.append(line.strip())

    ip = lines[14].split(':')

    cmd = 'ping {}'.format(ip[1].strip())
    output = con.send_command(cmd)
    print(output)

#!/usr/bin/python3

import re
import socket
import logging

logging.basicConfig(filename='campaign.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

log = logging.getLogger(__name__)


def search_port(dc_file):
    '''
    search ports from docker compose file.
    dc_file : docker compose file name.
    return : list of ports.
    '''

    with open(dc_file, 'r', encoding='utf-8') as f:
        dc_con = f.read()
        port_tag_reg = re.compile(r'ports:\s*(.*?)\s*container_name', flags=re.S | re.M | re.I)
        port_tag = port_tag_reg.findall(dc_con)
        ports = []
        for port in port_tag:
            p_list = re.findall(r'"(\d+):', port)
            _ = [ports.append(int(p)) for p in p_list]
        return ports


def pscan(port):
    '''
    scans port if it is open then return Ture otherwise False
    port : port number
    '''

    TCP_IP = '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    status = False

    try:
        s.bind((TCP_IP, port))
        status = True
    except OSError as e:
        log.warning(f'Port {port} is already in use.')
    finally:
        s.close()
    return status


def is_edgex_ports_open(ports):
    '''
    check edgex ports are open or not
    ports : list of ports
    return : True if all ports are open otherwise False
    '''
    open_port = []
    for port in ports:
        open_port.append(pscan(int(port)))
    res = all(p is True for p in open_port)
    if res:
        log.info('Edgex ports are opened.')


if __name__ == '__main__':
    p = search_port('docker-compose.yml')
    print(p)
    is_edgex_ports_open(p)

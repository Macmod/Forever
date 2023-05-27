#!/usr/bin/env python
import ipaddress as ip
import argparse
import random
import json
import sys
import os

def make_localfwd_str(loc_addr, loc_port, rem_addr, rem_port):
    return f'-L {loc_addr}:{loc_port}:{rem_addr}:{rem_port}'

if __name__ == '__main__':
    BANNER = (
        "d88888b  .d88b.  d8888b. d88888b db    db d88888b d8888b. \n"
        "88'     .8P  Y8. 88  `8D 88'     88    88 88'     88  `8D \n"
        "88ooo   88    88 88oobY' 88ooooo Y8    8P 88ooooo 88oobY' \n"
        "88~~~   88    88 88`8b   88~~~~~ `8b  d8' 88~~~~~ 88`8b   \n"
        "88      `8b  d8' 88 `88. 88.      `8bd8'  88.     88 `88. \n"
        "YP       `Y88P'  88   YD Y88888P    YP    Y88888P 88   YD \n"
    )

    parser = argparse.ArgumentParser(
        description='Forever (Forward Everything) is a simple tool that generates SSH command-line arguments to forward local addresses to multiple remote targets.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('targets', help='Input file containing target hostname:port pairs.')
    parser.add_argument('-r', '--range', help='Local CIDR range to use as address pool if the mode is address-based.', default='127.0.0.0/24')
    parser.add_argument('-m','--mode', help='Command-line generation mode to use.',
        default='seq_addrs',
        choices=[
            'random_addrs', 'random_ports',
            'seq_addrs', 'seq_ports'
        ]
    )
    parser.add_argument('-P', '--localport', help='Local port to use for all targets if the mode is address-based.', type=int, default=445)
    parser.add_argument('-A', '--localaddr', help='Local address to use for all targets if the mode is port-based.', default='127.0.0.1')
    parser.add_argument('-s', '--startport', help='Start port to use if the mode is port-based.', type=int, default=1024)
    parser.add_argument('-e', '--endport', help='End port to use if the mode is port-based.', type=int, default=65535)
    parser.add_argument('-v', '--verbose', help='Verbose mode.', action='store_true', default=False)

    args = parser.parse_args()

    local_port = args.localport
    local_addr = args.localaddr

    start_port = args.startport
    end_port = args.endport

    pool = args.range
    targetspath = args.targets

    mode = args.mode
    verbose = args.verbose

    if verbose:
        print(BANNER)

    with open(targetspath) as targetsfile:
        targets = targetsfile.read().splitlines()

    n_targets = len(targets)

    if end_port > 65535 or end_port < 1 or start_port > 65535 or start_port < 1:
        print('[-] Invalid ports specified!')
        exit(1)

    tunnel_strings = []

    if mode == 'seq_addrs':
        net = ip.IPv4Network(pool)
        hosts = list(net.hosts())

        #n_addrs = net.num_addresses - 2
        n_addrs = len(hosts)

        if verbose:
            print('[+] Selected mode: Sequential Addresses')
            print(f'[+] Pool: {hosts[0]} to {hosts[-1]}')
            print(f'[+] Pool Usage: {n_targets}/{n_addrs} addresses')

        if n_targets > n_addrs:
            print('[-] Your number of targets exceeds the number of available addresses in your pool!')
            exit(1)

        tunnel_strings = [
            make_localfwd_str(
                hosts[x],
                local_port,
                targets[x].split(':')[0],
                targets[x].split(':')[1]
            ) for x in range(len(targets))
        ]
    elif mode == 'seq_ports':
        n_addrs = end_port - start_port + 1

        if verbose:
            print('[+] Selected mode: Sequential Ports')
            print(f'[+] Pool: {start_port} to {end_port}')
            print(f'[+] Pool usage: {n_targets}/{n_addrs}')

        if n_targets > n_addrs:
            print('[-] Your number of targets exceeds the number of available addresses in your pool!')
            exit(1)

        tunnel_strings = [
            make_localfwd_str(
                local_addr,
                str(x+start_port),
                targets[x].split(':')[0],
                targets[x].split(':')[1]
            ) for x in range(len(targets))
        ]
    elif mode == 'random_addrs':
        net = ip.IPv4Network(pool)
        hosts = list(net.hosts())

        #n_addrs = net.num_addresses - 2
        n_addrs = len(hosts)
        
        if verbose:
            print('[+] Selected mode: Random Addresses')
            print(f'[+] Pool: {hosts[0]} to {hosts[-1]}')
            print(f'[+] Pool Usage: {n_targets}/{n_addrs} addresses')

        if n_targets > n_addrs:
            print('[-] Your number of targets exceeds the number of available addresses in your pool!')
            exit(1)

        random.shuffle(hosts)

        tunnel_strings = [
            make_localfwd_str(
                hosts.pop(),
                local_port,
                targets[x].split(':')[0],
                targets[x].split(':')[1]
            ) for x in range(len(targets))
        ]
    elif mode == 'random_ports':
        ports = list(range(start_port, end_port+1))
        random.shuffle(ports)

        n_addrs = len(ports) 

        if verbose:
            print('[+] Selected mode: Random Ports')
            print(f'[+] Pool: {start_port} to {end_port}')
            print(f'[+] Pool Usage: {n_targets}/{n_addrs} addresses')

        if n_targets > n_addrs:
            print('[-] Your number of targets exceeds the number of available addresses in your pool!')
            exit(1)

        tunnel_strings = [
            make_localfwd_str(
                local_addr,
                ports.pop(),
                targets[x].split(':')[0],
                targets[x].split(':')[1]
            ) for x in range(len(targets))
        ]

    ssh_args = ' '.join(tunnel_strings)

    if verbose:
        print('[+] Result:')

    print(ssh_args)

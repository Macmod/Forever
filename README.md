# Forever

Forever (Forward Everything) is a simple tool that generates SSH command-line arguments to forward local addresses to multiple remote targets.

When you need to access multiple remote services through an SSH-enabled proxy server, there are reasons why you might not want to use SSH's dynamic port forwarding with `-D`, like when you need to access these services through desktop applications that don't offer SOCKS support. In that case, one is left with the option of forwarding local ports to remote targets using SSH's `-L` switches, but with a large list of targets this approach becomes exhaustive.

The `forever.py` tool is a simple utility to fix that - it generates `-L` switches through a variety of methods for multiple targets to be forwarded through SSH, only depending on the amount of local addresses you have available.

This "trick" might be useful for cases where you want to quickly access a big but reasonable number of services, and don't want to write the `-L` switches by hand. You can bind up to 254 services to your loopback addresses, up to 65535 services to your loopback ports, or use addresses/ports from other network interfaces you might have available on your host for that task.

# Usage

## Asciicast
[![asciicast](https://asciinema.org/a/qI49iOKQfbBM5JldFMEjgMFCX.svg)](https://asciinema.org/a/qI49iOKQfbBM5JldFMEjgMFCX)

## Sequential Addresses
```bash
$ python3 forever.py <targetsfile>
```

## Random Addresses
```bash
$ python3 forever.py --mode random_addrs <targetsfile>
```

## Sequential Ports
```bash
$ python3 forever.py --mode seq_ports <targetsfile>
```

## Random Ports
```bash
$ python3 forever.py --mode random_ports <targetsfile>
```

## Additional Options
* `-r CIDR` or `--range` - Custom CIDR range for address modes (default: `127.0.0.0/24`).
* `-P PORT` or `--localport` - Custom local port for address modes (default: `445`).
* `-A address` or `--localaddr` - Custom local address for port modes (default: `127.0.0.1`).
* `-s PORT` or `--startport` - Custom start port for port modes (default: `1024`).
* `-e PORT` or `--endport` - Custom end port for port modes (default: `65535`).
* `-v` or `--verbose` - Enable verbose mode.

# License
The MIT License (MIT)

Copyright (c) 2023 Artur Henrique Marzano Gonzaga

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

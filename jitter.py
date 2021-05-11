"""
Calculate Jitter
"""
import platform
import subprocess
import sys
import ipaddress
import signal
import re
from decimal import Decimal
from time import sleep

def ping_results(ip_in: str) -> []:
    """
    ping and provide results
    """
    count = 5
    if platform.system() == 'Windows':
        count_parameter = '-n'
        start = 2
        regex_text = r"(?<=time=)(\d)"
    else:
        count_parameter = '-c'
        start = 1
        regex_text = r"(?<=time=)(\w+.\w+)"
    ping_result = subprocess.run(['ping', ip_in, count_parameter, str(count)],
                                 stdout=subprocess.PIPE).stdout.decode('utf-8')

    lines = ping_result.split('\n')

    try:
        times = [re.findall(regex_text, x)[0] for x in lines[start:count + 1]]
    except:
        times = []
    return times

def calc_jitter(ip_in: str):
    """
    Calculate jitter for given ip
    """
    if ip_in is None:
        return
    while True:
        results = ping_results(ip_in)
        total = 0
        for i in range(len(results[:-1])):
            diff = abs(Decimal(results[i + 1]) - Decimal(results[i]))
            total += diff
        if not results:
            jitter = -10
            sleep(5)
        else:
            jitter = total / len(results)
        print("IP/Host: {} Jitter: {}".format(ip_in, jitter))

def signal_handler(sig, frame):
    """
    handle signal
    """
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

try:
    ip_arg = ipaddress.ip_address(sys.argv[1])
    ip_str = sys.argv[1]
    print('%s is a correct IP%s address.' % (ip_arg, ip_arg.version))
    calc_jitter(ip_str)
except ValueError:
    print('address/netmask is invalid: %s' % sys.argv[1])
except IndexError:
    print('Usage : %s ip' % sys.argv[0])




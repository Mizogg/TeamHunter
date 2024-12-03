import bit
import ctypes
import platform
import sys
import os
import random
import argparse
import signal

###############################################################################
parser = argparse.ArgumentParser(description='This tool uses the Kangaroo algorithm for searching a public key in the given range using multiple CPUs', 
                                 epilog='Enjoy the program! :) ')
parser.version = '15112022'
parser.add_argument("-p", "--pubkey", help="Public Key in hex format (compressed or uncompressed)", required=True)
parser.add_argument("-keyspace", help="Keyspace Range (hex) to search from min:max. default=1:order of curve", action='store')
parser.add_argument("-ncore", help="Number of CPU cores to use. default = Total-1", action='store')
parser.add_argument("-n", help="Total range search in 1 loop. default=72057594037927935", action='store')
parser.add_argument("-rand", help="Start from a random value in the given range from min:max and search 0XFFFFFFFFFFFFFF values then again take a new random", action="store_true")
parser.add_argument("-rand1", help="First start from a random value, then go fully sequential, in the given range from min:max", action="store_true")
parser.add_argument("-dp", help="Value for DP parameter", type=int)
parser.add_argument("-mx", help="Value for MaxStep parameter", type=int)

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)


def main():
    def run_cpu_kangaroo(ice, start_range_int, end_range_int, dp, ncpu, mx, upub_bytes):
        st_hex = hex(start_range_int)[2:].encode('utf8')
        en_hex = hex(end_range_int)[2:].encode('utf8')
        res = (b'\x00') * 32
        ice.run_cpu_kangaroo(st_hex, en_hex, dp, ncpu, mx, res, upub_bytes)
        return res

    def pub2upub(pub_hex):
        x = int(pub_hex[2:66], 16)
        if len(pub_hex) < 70:
            y = bit.format.x_to_y(x, int(pub_hex[:2], 16) % 2)
        else:
            y = int(pub_hex[66:], 16)
        return bytes.fromhex('04' + hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))

    def randk(a, b, flag_random):
        if flag_random:
            random.seed(random.randint(1, 2 ** 256))
            return random.SystemRandom().randint(a, b)
        else:
            if lastitem == 0:
                return a
            elif lastitem > b:
                print('[+] Range Finished')
                exit()
            else:
                return lastitem + 1

    def handler(signal_received, frame):
        # Handle any cleanup here
        print('\nSIGINT or CTRL-C detected. Exiting gracefully. BYE')
        exit(0)

    global ice  # Declare ice as global to access throughout the script

    args = parser.parse_args()

    ss = args.keyspace if args.keyspace else '1:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140'
    flag_random = True if args.rand else False
    flag_random1 = True if args.rand1 else False
    ncore = int(args.ncore) if args.ncore else platform.os.cpu_count() - 1
    increment = int(args.n) if args.n else 72057594037927935
    dp = int(args.dp) if args.dp else 5
    mx = int(args.mx) if args.mx else 2
    public_key = args.pubkey
    if flag_random1:
        flag_random = True

    a, b = ss.split(':')
    a = int(a, 16)
    b = int(b, 16)
    lastitem = 0

    if platform.system().lower().startswith('win'):
        pathdll = os.path.realpath('Kangaroo_CPU.dll')
        ice = ctypes.CDLL(pathdll)
    elif platform.system().lower().startswith('lin'):
        pathdll = os.path.realpath('Kangaroo_CPU.so')
        ice = ctypes.CDLL(pathdll)
    else:
        print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
        sys.exit()

    ice.run_cpu_kangaroo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
    ice.init_kangaroo_lib()

    upub = pub2upub(public_key)

    if flag_random1:
        print('[+] Search Mode: Random Start then Continuous Range Search from it')
    elif flag_random:
        print('[+] Search Mode: Random Start after every Range 0XFFFFFFFFFFFFFF key search')
    else:
        print('[+] Search Mode: Range search Continuous in the given range')

    print(f"Initial Range: {a} to {b}")
    range_st = randk(a, b, flag_random)  # start from
    range_en = range_st + increment

    print(f"Start Range: {hex(range_st)}")
    print(f"End Range: {hex(range_en)}")

    if flag_random1:
        flag_random = False

    print('[+] Working on Pubkey:', upub.hex())
    sys.stdout.flush()
    print('[+] Using  [Number of CPU Threads: {}] [DP size: {}] [MaxStep: {}] [Increment: {}]'.format(ncore, dp, mx, increment))
    print(f'[+] Please Wait Increment Value : {increment} . The Larger the increment means longer the pause but increase the speed.')
    sys.stdout.flush()

    while True:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print('\r[+] Scanning Range          ', hex(range_st), ':', hex(range_en))
        print('[+] Using  [Number of CPU Threads: {}] [DP size: {}] [MaxStep: {}] [Increment: {}]'.format(ncore, dp, mx, increment))
        sys.stdout.flush()
        pvk_found = run_cpu_kangaroo(ice, range_st, range_en, dp, ncore, mx, upub)
        
        # Log the scanned range
        with open('scannedkeys.txt', 'a') as ab:
            ab.write(f"{hex(range_st)}:{hex(range_en)}\n")
        
        # Debugging print
        print(f"Private key found (hex): {pvk_found.hex()}")

        if int(pvk_found.hex(), 16) != 0:
            print('\n============== KEYFOUND ==============')
            print('Kangaroo FOUND PrivateKey : 0x' + pvk_found.hex())
            print('======================================')
            sys.stdout.flush()
            with open('KEYFOUNDKEYFOUND.txt', 'a') as fw:
                fw.write('Kangaroo FOUND PrivateKey : 0x' + pvk_found.hex() + '\n')
            break
        else:
            print("[+] No key found in this range.")

        lastitem = range_en
        range_st = randk(a, b, flag_random)
        range_en = range_st + increment
        print('', end='\r')
        sys.stdout.flush()

    print('[+] Program Finished')
    sys.stdout.flush()


if __name__ == "__main__":
    main()

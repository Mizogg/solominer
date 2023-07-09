#!/usr/bin/env python  

from signal import signal, SIGINT
import context as ctx 
import traceback 
import threading
import requests 
import binascii
import hashlib
import logging
import random
import socket
import time
import json
import os, sys, platform

is_windows = True if platform.system() == "Windows" else False

if is_windows:
    os.system("title Mizogg @ github.com/Mizogg")

def red(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded

def win_colour(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 20
        for character in line:
            green += 3
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded
    
def blue(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        faded += "\n"
    return faded

def water(text):
    os.system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded

soloxminer = f'''
███╗   ██╗ ██████╗ ████████╗     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
████╗  ██║██╔═══██╗╚══██╔══╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
██╔██╗ ██║██║   ██║   ██║       ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
██║╚██╗██║██║   ██║   ██║       ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║ ╚████║╚██████╔╝   ██║       ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═══╝ ╚═════╝    ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝


        ██████╗ ██╗   ██╗████████╗     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ███╗   ██╗
        ██╔══██╗██║   ██║╚══██╔══╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗████╗  ██║
        ██████╔╝██║   ██║   ██║       ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██╔██╗ ██║
        ██╔══██╗██║   ██║   ██║       ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██║╚██╗██║
        ██████╔╝╚██████╔╝   ██║       ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝██║ ╚████║
        ╚═════╝  ╚═════╝    ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝  ╚═══╝

                                                                                
            ███████╗ ██████╗ ██╗      ██████╗     ███╗   ███╗██╗███╗   ██╗███████╗██████╗ 
            ██╔════╝██╔═══██╗██║     ██╔═══██╗    ████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
            ███████╗██║   ██║██║     ██║   ██║    ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
            ╚════██║██║   ██║██║     ██║   ██║    ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
            ███████║╚██████╔╝███████╗╚██████╔╝    ██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
            ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

                                      ___            ___
                                     (o o)          (o o)
                                    (  V  ) MIZOGG (  V  )
                                    --m-m------------m-m--
                                  © mizogg.co.uk 2018 - 2023
                                   solo_miner.py CryptoHunter

                                        PROJECT Mizogg
                                 
                                {red(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}
'''


INPUTNEEDED = '''

  ,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
  |esc| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | + | ' | <-    |
  |---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
  | ->| | Q | W | E | R | T | Y | U | I | O | P | ] | ^ |     |
  |-----',--',--',--',--',--',--',--',--',--',--',--',--'|    |
  | Caps | A | S | D | F | G | H | J | K | L | \ | [ | * |    |
  |----,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'---'----|
  |    | < | Z | X | C | V | B | N | M | , | . | - |          |
  |----'-,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
  | ctrl |🪟| alt |                          |altgr |  | ctrl |
  '------'  '-----'--------------------------'------'  '------'    

'''

print(water(soloxminer), end="")

address = str('3JKyVkRtxDrXEMtZY6Fy53VmvMAT6LKBo8')
print(red('\n------------------------------------------------------------------------------'), end="")
print(red(f' Your Bitcoin Wallet Address Added For Mining Now Starting ... {address} '), end="")
print(red('------------------------------------------------------------------------------'), end="")

time.sleep(2)

def handler(signal_received, frame):
    ctx.fShutdown = True
    print(red('Terminating miner, please wait..'), end="")

def logg(msg):
    logging.basicConfig(level=logging.INFO, filename="miner.log", format='%(asctime)s %(message)s') # include timestamp
    logging.info(msg)

def get_current_block_height():
    r = requests.get('https://blockchain.info/latestblock')
    return int(r.json()['height'])

def check_for_shutdown(t):
    n = t.n
    if ctx.fShutdown:
        if n != -1:
            ctx.listfThreadRunning[n] = False
            t.exit = True

class ExitedThread(threading.Thread):
    def __init__(self, arg, n):
        super(ExitedThread, self).__init__()
        self.exit = False
        self.arg = arg
        self.n = n

    def run(self):
        self.thread_handler(self.arg, self.n)
        pass

    def thread_handler(self, arg, n):
        while True:
            check_for_shutdown(self)
            if self.exit:
                break
            ctx.listfThreadRunning[n] = True
            try:
                self.thread_handler2(arg)
            except Exception as e:
                logg("ThreadHandler()")
                logg(e)
            ctx.listfThreadRunning[n] = False

            time.sleep(5)
            pass

    def thread_handler2(self, arg):
        raise NotImplementedError("must impl this func")

    def check_self_shutdown(self):
        check_for_shutdown(self)

    def try_exit(self):
        self.exit = True
        ctx.listfThreadRunning[self.n] = False
        pass

def bitcoin_miner(t, restarted=False):

    if restarted:
        logg('[*] Bitcoin Miner restarted')
        print(red('[*] Bitcoin Miner restarted'), end="")
        time.sleep(10)

    target = (ctx.nbits[2:]+'00'*(int(ctx.nbits[:2],16) - 3)).zfill(64)
    extranonce2 = hex(random.randint(0,2**32-1))[2:].zfill(2*ctx.extranonce2_size)

    coinbase = ctx.coinb1 + ctx.extranonce1 + extranonce2 + ctx.coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in ctx.merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()
    merkle_root = binascii.hexlify(merkle_root).decode()
    merkle_root = ''.join([merkle_root[i]+merkle_root[i+1] for i in range(0,len(merkle_root),2)][::-1])

    work_on = get_current_block_height()
    print(red(f'\nWorking on current Network height {work_on} '), end="")
    print(red(f'\nCurrent TARGET = {target} '), end="")

    ctx.nHeightDiff[work_on+1] = 0 

    _diff = int("00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)

    logg('[*] Working to solve block with height {}'.format(work_on+1))
    print(purple('\n[*] Working to solve block with height {}'.format(work_on+1)) + "\033[38;2;148;0;230m")

    z = 0
    while True:
        t.check_self_shutdown()
        if t.exit:
            break

        if ctx.prevhash != ctx.updatedPrevHash:
            logg('[*] New block {} detected on network '.format(ctx.prevhash))
            logg('[*] Best difficulty will trying to solve block {} was {}'.format(work_on+1, ctx.nHeightDiff[work_on+1]))
            print(red('[*] New block {} detected on network '.format(ctx.prevhash)), end="")
            print(win_colour('[*] Best difficulty will trying to solve block {} was {}'.format(work_on+1, ctx.nHeightDiff[work_on+1])), end="")
            ctx.updatedPrevHash = ctx.prevhash
            bitcoin_miner(t, restarted=True)
            break 

        nonce   = hex(random.randint(0,2**32-1))[2:].zfill(8)
        blockheader = ctx.version + ctx.prevhash + merkle_root + ctx.ntime + ctx.nbits + nonce +\
        '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'
        hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
        hash = binascii.hexlify(hash).decode()
        z += 1
        if hash.startswith('000000000000000000000'): logg('[*] New hash: {} for block {}'.format(hash, work_on+1))
        print('',str(z),' HASH :', ' 000000000000000000000{}'.format(hash), end='\r')
        z += 1
        
        if hash.startswith('000000000000000000'): logg('[*] New hash: {} for block {}'.format(hash, work_on+1))
        print('',str(z), 'HASH :', ' 000000000000000000{}'.format(hash), end='\r')
        z += 1

        if hash.startswith('000000000000000'): logg('[*] New hash: {} for block {}'.format(hash, work_on+1))
        print('',str(z), 'HASH :', ' 000000000000000{}'.format(hash), end='\r')
        z += 1

        if hash.startswith('000000000000'): logg('[*] New hash: {} for block {}'.format(hash, work_on+1))
        print('',str(z),'HASH :', ' 000000000000{}'.format(hash), end='\r')
        z += 1

        if hash.startswith('0000000'): logg('[*] New hash: {} for block {}'.format(hash, work_on+1))
        print('',str(z),'HASH :', ' 0000000{}'.format(hash), end='\r')
        z += 1

        this_hash = int(hash, 16)
        difficulty = _diff / this_hash

        if ctx.nHeightDiff[work_on+1] < difficulty:
            ctx.nHeightDiff[work_on+1] = difficulty

        if hash < target :
            print(water('[*] New block mined'), end="")
            logg('[*] Block {} solved.'.format(work_on+1))
            logg('[*] Block hash: {}'.format(hash))
            logg('[*] Blockheader: {}'.format(blockheader))            
            payload = bytes('{"params": ["'+address+'", "'+ctx.job_id+'", "'+ctx.extranonce2 \
                +'", "'+ctx.ntime+'", "'+nonce+'"], "id": 1, "method": "mining.submit"}\n', 'utf-8')
            logg('[*] Payload: {}'.format(payload))
            sock.sendall(payload)
            ret = sock.recv(1024)
            logg('[*] Pool response: {}'.format(ret))
            print('[*] Block {} solved.'.format(work_on+1))
            print('[*] Block hash: {}'.format(hash))
            print('[*] Blockheader: {}'.format(blockheader)) 
            print('[*] Payload: {}'.format(payload))
            return True

def block_listener(t):
    sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('solo.ckpool.org', 3333))
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    ctx.sub_details,ctx.extranonce1,ctx.extranonce2_size = response['result']
    sock.sendall(b'{"params": ["'+address.encode()+b'", "password"], "id": 2, "method": "mining.authorize"}\n')
    response = b''
    while response.count(b'\n') < 4 and not(b'mining.notify' in response):response += sock.recv(1024)
    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]
    ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = responses[0]['params']
    ctx.updatedPrevHash = ctx.prevhash

    while True:
        t.check_self_shutdown()
        if t.exit:
            break
        response = b''
        while response.count(b'\n') < 4 and not(b'mining.notify' in response):response += sock.recv(1024)
        responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]     

        if responses[0]['params'][1] != ctx.prevhash:
            ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = responses[0]['params']

class CoinMinerThread(ExitedThread):
    def __init__(self, arg=None):
        super(CoinMinerThread, self).__init__(arg, n=0)

    def thread_handler2(self, arg):
        self.thread_bitcoin_miner(arg)

    def thread_bitcoin_miner(self, arg):
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try:
            ret = bitcoin_miner(self)
            logg("[*] Miner returned %s\n\n" % "true" if ret else"false")
        except Exception as e:
            logg("[*] Miner()")
            logg(e)
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False

    pass  

class NewSubscribeThread(ExitedThread):
    def __init__(self, arg=None):
        super(NewSubscribeThread, self).__init__(arg, n=1)

    def thread_handler2(self, arg):
        self.thread_new_block(arg)

    def thread_new_block(self, arg):
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try:
            ret = block_listener(self)
        except Exception as e:
            logg("[*] Subscribe thread()")
            logg(e)
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False

    pass  

def StartMining():
    subscribe_t = NewSubscribeThread(None)
    subscribe_t.start()
    logg("[*] Subscribe thread started.")
    print(win_colour('[*] Subscribe thread started.'), end="")
    time.sleep(1)

    miner_t = CoinMinerThread(None)
    miner_t.start()
    logg("[*] Bitcoin miner thread started")

    print(win_colour('[*] Bitcoin Miner Started'), end="")

if __name__ == '__main__':
    signal(SIGINT, handler)
    StartMining()
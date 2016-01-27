#!/usr/bin/env python

import logging
import socket
import subprocess
from logging.handlers import TimedRotatingFileHandler

LOG_FILENAME = '/var/log/wolkodi.log'
UDP_PORT = 9

def config_log(log_filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(log_filename, when="d", interval=30, backupCount=5)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.bind(("0.0.0.0", UDP_PORT)) # could also use "0.0.0.0"

    while True:
        data, addr = sock.recvfrom(512) # buffer size is 512 bytes
        logger.info("UPD package from IP '%s'", addr[0])
        p = subprocess.Popen(["cat", "/etc/issue"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        if 'Arch Linux' in str(out):
            if "Active: active (running)" in str(out):
                logger.info("kodi is already runnning. Nothing to do")
            else:
                logger.info("Starting kodi...")
                subprocess.Popen(['systemctl','start','kodi'])
                logger.info("kodi has been started :-)")
        else:
            logger.info("Starting kodi (Raspbian)...")
            subprocess.Popen(["/usr/bin/kodi"], stdout=subprocess.PIPE)
            logger.info("kodi has been started :-)")
            

if __name__ == "__main__":
    try:
        logger = config_log(LOG_FILENAME)
        main()
    except Exception as e:
        logger.error(e)

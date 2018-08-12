#!/usr/bin/env python3

import logging
import time
from subprocess import Popen
from datetime import datetime

from webcam import PATH, EXT


def loop():
    while True:
        files = sorted(list(PATH.glob("*." + EXT)))
        print(files)
        break
        time.sleep(10)



if __name__ == '__main__':
    logging.basicConfig(filename="convert.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("=== Start")
    loop()
    logging.info("=== End")



#!/usr/bin/env python3

import logging
import time
from subprocess import Popen
from datetime import datetime

from webcam import PATH, EXT


D1 = "120fps"


def convert(f):
    logging.info("Converting %s" % f)
    cmd_line = "exec ffmpeg -i " + str(f)
    cmd_line += " -hide_banner"
    cmd_line += " -r 120"
    cmd_line += " -filter:v \"setpts=0.1*PTS\""
    cmd_line += " " + str(PATH / D1 / f.name)

    logging.info("New convert: %s" % cmd_line)
    Popen(cmd_line, shell=True).wait()


def loop():
    while True:
        # get all files except last two
        converted = sorted(list((PATH / D1).glob("*." + EXT)))
        converted = [c.name for c in converted]
        to_convert = sorted(list(PATH.glob("*." + EXT)))[:-2]
        for file in to_convert:
            if file.name not in converted:
                convert(file)
        break
        time.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(filename="convert.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("=== Start")
    loop()
    logging.info("=== End")



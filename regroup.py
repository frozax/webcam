#!/usr/bin/env python3

import logging
import time
from subprocess import Popen
from datetime import datetime

from webcam import PATH, EXT
from convert import D1


D2 = "regroup"
VID_PER_GROUP = 8


def regroup(fs):
    """takes 8 videos and group them in one"""
    cmd_line = "exec ffmpeg"
    for f in fs:
        cmd_line += " -i " + str(f)
    cmd_line += " -hide_banner"
    cmd_line += " " + str(PATH / D2 / fs[0].name)



def loop():
    while True:
        # get all files except last two
        to_regroup = sorted(list((PATH / D1).glob("*." + EXT)))[:-2]
        # only get file if it's multiple of VID_PER_GROUP and there are enough
        # to regroup
        print(to_regroup)
        for f in to_regroup:

        regrouped = sorted(list((PATH / D2).glob("*." + EXT)))
        for file in to_convert:
            if file.name not in converted:
                convert(file)
        break
        time.sleep(10)



if __name__ == '__main__':
    logging.basicConfig(filename="regroup.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("=== Start")
    loop()
    logging.info("=== End")



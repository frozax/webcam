#!/usr/bin/env python3

import logging
import time
from subprocess import Popen
from datetime import datetime

from webcam import PATH_REGROUP, PATH_120, EXT


D2 = "regroup"
VID_PER_GROUP = 8


def regroup(fs):
    FINAL_SIZE = "960x720"
    """takes 8 videos and group them in one"""
    cmd_line = "exec ffmpeg"
    for f in fs:
        cmd_line += " -i " + str(f)
    cmd_line += " -hide_banner"

    cmd_line += " -filter_complex \"color=c=white:size=" + FINAL_SIZE + " [base0];"
    for i, f in enumerate(fs):
        cmd_line += " [%d:v] setpts=PTS-STARTPTS, scale=320x240 [v%d];" % (i, i)
    for i, f in enumerate(fs):
        x = (i % 3) * 320
        y = (i // 3) * 240
        cmd_line += " [base%d][v%d] overlay=x=%d:y=%d" % (i, i, x, y)
        #if i != len(fs) - 1:
        # prepare next filter
        cmd_line += " [base%d];" % (i + 1)
    # speed up x8
    cmd_line += " [base%d] setpts=0.125*PTS" % (i+1)

    cmd_line += "\""


    cmd_line += " " + str(PATH_REGROUP / fs[0].name)
    print(cmd_line)
    logging.info("New regroup: %s" % cmd_line)
    Popen(cmd_line, shell=True).wait()


def loop():
    while True:
        # get all files except last one
        regrouped_files = sorted(list((PATH_REGROUP).glob("*." + EXT)))
        regrouped_files = [f.name for f in regrouped_files]
        regroup_files = sorted(list((PATH_120).glob("*." + EXT)))[:-1]
        # don't go to the end, because we need to have enough input
        for i, f in enumerate(regroup_files[:-VID_PER_GROUP]):
            ext_len = len("." + EXT)
            end = f.name[-2-ext_len:-ext_len]
            if f.name in regrouped_files:
                continue
            if int(end) % VID_PER_GROUP == 0:
                regroup(regroup_files[i:i+VID_PER_GROUP])

        time.sleep(10)



if __name__ == '__main__':
    logging.basicConfig(filename="regroup.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("=== Start")
    loop()
    logging.info("=== End")



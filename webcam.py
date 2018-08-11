#!/usr/bin/env python3

import logging
import time
import pathlib
import threading
from subprocess import Popen
from datetime import datetime

BITRATE = "10000k"
PATH = pathlib.Path("/media/freebox/webcam")

def compute_name_from_now():
    #return datetime.now().strftime("%Y%m%d-%H%M")  # debug: use minute and second dizaines
    return datetime.now().strftime("%Y%m%d-%H")


def compute_date_from_name(name):
    return datetime.now()


capture_process = None
def start_capture(name):
    global capture_process
    if capture_process:
        logging.info("Stop capture: %s" % capture_process)
        capture_process.kill()
        ret = capture_process.wait()
        logging.info("Stopped with return code: %s" % ret)

    cmd_line = "exec ffmpeg -f v4l2"
    cmd_line += " -video_size 640x480"
    cmd_line += " -i /dev/video0"
    cmd_line += " -vf \"drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeMono.ttf: text='%{localtime}': x=w-tw: y=h-(1*lh): fontcolor=white: box=1: boxcolor=0x00000000@1\""
    #cmd_line += " -codec h264"
    cmd_line += " -crf 21"
    #cmd_line += " -b:v " + BITRATE
    cmd_line += " " + str(PATH) + "/" + name + ".mkv"

    logging.info("New capture: %s", cmd_line)
    capture_process = Popen(cmd_line, shell=True)


def loop():
    current_run = None
    while True:
        expected_run = compute_name_from_now()
        if expected_run != current_run:
            current_run = expected_run
            logging.info("New run: %s", current_run)
            start_capture(expected_run)
        time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(filename="webcam.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("=== Start")
    loop()
    logging.info("=== End")



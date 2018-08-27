#!/usr/bin/env python3

import logging
import shutil
import os
import time
from subprocess import Popen
from datetime import datetime
from pathlib import Path

from webcam import PATH_120, PATH_RAW, EXT, RAW_EXT


def convert(f_prefix):
    logging.info("convert(%s)" % f_prefix)
    i = 0
    tmp_path = Path("/tmp/motion")
    shutil.rmtree(str(tmp_path))
    os.mkdir(str(tmp_path))
    source_files = sorted(PATH_RAW.glob(f_prefix + "*." + RAW_EXT))
    logging.info("Copying %d files to convert location %s" % (len(source_files), str(tmp_path)))
    for f in source_files:
        new_name = "%s/%s%05d.%s" % (str(tmp_path), f_prefix, i, RAW_EXT)
        shutil.copy(str(f), new_name)
        i += 1
    logging.info("Converting %s (%d files)" % (f_prefix, i))
    cmd_line = "exec ffmpeg -i %s/%s%%05d.%s" % (str(tmp_path), f_prefix, RAW_EXT)
    cmd_line += " -hide_banner"
    cmd_line += " -r 120"
    #cmd_line += " -filter:v \"setpts=0.1*PTS\""
    cmd_line += " " + str(PATH_120 / (f_prefix + "." + EXT))
    logging.info("New convert: %s" % cmd_line)
    if Popen(cmd_line, shell=True).wait() == 0:
        # remove source files
        for f in source_files:
            f.unlink()
    else:
        logging.error("Error creating file, not deleting sources")
    logging.info("Done")


def loop():
    while True:
        # get all files except last two
        # get oldest and newest image, if it's not the same day, we can convert
        # the previous day if it's not already done
        # Copy the files to /tmp and number them properly
        converted = sorted(list((PATH_120).glob("*." + EXT)))
        converted = [c.name[:-1-len(EXT)] for c in converted]
        to_convert = []
        for img_file in PATH_RAW.glob("*." + RAW_EXT):
            short_name = img_file.name[:-13]
            if short_name not in to_convert:
                to_convert.append(short_name)
        to_convert = sorted(to_convert)
        print(to_convert, converted)
        for f in to_convert[:-1]:  # ignore last date, it's the current one
            if f not in converted:
                convert(f)
        time.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(filename="convert.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("=== Start")
    loop()
    logging.info("=== End")



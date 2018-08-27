#!/usr/bin/env python3

import pathlib
from datetime import datetime

PATH_RAW = pathlib.Path("/media/freebox/webcam/motion")
PATH_120 = pathlib.Path("/home/francois/webcam/120fps")
PATH_REGROUP = pathlib.Path("/media/freebox/webcam/regroup")
EXT = "mkv"
RAW_EXT = "jpg"

def compute_name_from_now():
    #return datetime.now().strftime("%Y%m%d-%H%M")  # debug: use minute and second dizaines
    return datetime.now().strftime("%Y%m%d-%H")


def compute_date_from_name(name):
    return datetime.now()


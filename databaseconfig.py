#!/usr/bin/env python3

import preprocessing

mysql = {
    "host": "localhost",
    "user": "root",
    "password": "your password",
    "database": "database",
}
preprocessing_queue = [
    preprocessing.scale_and_center,
    preprocessing.dot_reduction,
    preprocessing.connect_lines,
]
use_anonymous = True

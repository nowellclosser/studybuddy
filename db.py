import sqlite3

import common

def get_connection():
    con = sqlite3.connect(common.STUDYBUDDY_DB)
    con.row_factory = sqlite3.Row
    return con

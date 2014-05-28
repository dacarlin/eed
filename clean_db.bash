#!/usr/local/bin/bash
sqlite3 db.sqlite3 "DROP TABLE enter_entry"
python3 manage.py sqlall enter
python3 manage.py syncdb

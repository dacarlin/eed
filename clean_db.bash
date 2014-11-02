#!/usr/local/bin/bash
sqlite3 db.sqlite3 "DROP TABLE enter_dataentry"
python3 manage.py sqlall enter
python3 manage.py syncdb

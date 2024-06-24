import sqlite3
import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Connection

def get_nodes(self):
    tmp = Connection.objects.all()
    host = tmp.values('id', 'type', 'host')
    values = []
    for i in host:
        if i['type'] == 'Qemu':
            values.append(i['host'])
    # getattr(tmp, 'host')
    # host = tmp.__dict__
    # print(f'hooooooooooooooooooooooooooooooooost {values}')
    return values


import sqlite3
import os
import sys
import django
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Connection


def get_nodes(self):
    """
    Retrieves a list of host addresses for all Qemu type connections from the database.

    This function queries the Connection model for all entries, filtering for those of type 'Qemu'.
    It then extracts the 'host' field from each qualifying entry and compiles a list of these host addresses.

    Returns:
        list: A list of host addresses (strings) for all Qemu type connections.
    """
    tmp = Connection.objects.all()
    host = tmp.values('id', 'type', 'host')
    values = []
    for i in host:
        if i['type'] == 'Qemu':
            values.append(i['host'])
    return values


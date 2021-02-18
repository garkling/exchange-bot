from typing import List, Tuple
import sqlite3

connection = sqlite3.connect('db.db')
cursor = connection.cursor()


def update(data: List[Tuple], table='rates') -> None:
    with connection:
        for cur_name, rate in data:
            cursor.execute(f'UPDATE {table} '
                           'SET rate=? '
                           'WHERE codename=?', (rate, cur_name))


def fetchall(columns: List, table='rates') -> List[Tuple]:
    joined = ', '.join(columns)
    cursor.execute(f'SELECT {joined} '
                   f'FROM {table}')

    return cursor.fetchall()



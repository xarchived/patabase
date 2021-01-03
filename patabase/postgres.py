from typing import Any, List

import psycopg2
import psycopg2.extras


class Database(object):
    def __init__(self, user: str, password: str, database: str, host: str = 'localhost', port: int = 5432):
        self._con = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database)

    def _execute(self, cur, query, parameters=None):
        try:
            cur.execute(query, parameters)
        except Exception as e:
            self._con.rollback()
            raise e

    def _callproc(self, cur, func_name, parameters=None):
        try:
            cur.callproc(func_name, parameters)
        except Exception as e:
            self._con.rollback()
            raise e

    def perform(self, sql: str, *args: Any) -> int:
        with self._con.cursor() as cur:
            self._execute(cur, sql, args)
            self._con.commit()

            return cur.rowcount

    def select(self, sql: str, *args: Any) -> List[dict]:
        rows = []
        with self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            self._execute(cur, sql, args)
            self._con.commit()

            for row in cur.fetchall():
                rows.append(dict(row))

        return rows

    def procedure(self, func_name: str, **parameters: Any) -> int:
        with self._con.cursor() as cur:
            self._callproc(cur, func_name, parameters)
            self._con.commit()

            return cur.rowcount

    def function(self, func_name: str, **parameters: Any) -> List[dict]:
        rows = []
        with self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            self._callproc(cur, func_name, parameters)
            self._con.commit()

            for row in cur.fetchall():
                rows.append(dict(row))

        return rows

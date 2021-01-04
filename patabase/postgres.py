from time import sleep
from typing import Any, List

import psycopg2
import psycopg2.extras


def error_handler(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        max_retries = self.max_retries
        retry_delay = self.retry_delay

        for i in range(1, max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                err = str(e)
                if not self._con.closed:
                    self._con.rollback()
                if i == max_retries:
                    raise e
                if err == 'SSL SYSCALL error: EOF detected\n':
                    continue
                if err == 'connection already closed':
                    sleep(retry_delay * i)
                    self._con = self._connect()
                    continue

                raise e

    return wrapper


class Database(object):
    def __init__(self, user: str, password: str, database: str, host: str = 'localhost', port: int = 5432,
                 max_retries: int = 5, retry_delay: int = 5):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self._con = self._connect()

    def _connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database)

    @error_handler
    def perform(self, sql: str, *args: Any) -> int:
        with self._con.cursor() as cur:
            cur.execute(sql, args)
            self._con.commit()

            return cur.rowcount

    @error_handler
    def select(self, sql: str, *args: Any) -> List[dict]:
        rows = []
        with self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, args)
            self._con.commit()

            for row in cur.fetchall():
                rows.append(dict(row))

        return rows

    @error_handler
    def procedure(self, func_name: str, **parameters: Any) -> int:
        with self._con.cursor() as cur:
            cur.callproc(func_name, parameters)
            self._con.commit()

            return cur.rowcount

    @error_handler
    def function(self, func_name: str, **parameters: Any) -> List[dict]:
        rows = []
        with self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.callproc(func_name, parameters)
            self._con.commit()

            for row in cur.fetchall():
                rows.append(dict(row))

        return rows

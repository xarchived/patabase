from typing import Any, Iterator

import pyodbc


class Database(object):
    def __init__(self, user: str, password: str, database: str, host: str = 'localhost', port: int = 1433):
        for driver in pyodbc.drivers():
            self._con = None
            if 'SQL Server' in driver:
                self._con = pyodbc.connect(
                    '',
                    driver=driver,
                    server=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database)

        if not self._con:
            raise Exception('Driver not found')

    def _execute(self, cursor: pyodbc.Cursor, query: str, parameters: tuple) -> None:
        try:
            cursor.execute(query, parameters)
        except Exception as e:
            self._con.rollback()
            raise e

    @staticmethod
    def _exec_sql(func_name: str, parameters: dict) -> str:
        args = [f'@{k}=?' for k in parameters]

        sql = f'''
            exec {func_name} {', '.join(args)}
        '''

        return sql

    def perform(self, sql: str, *args: Any) -> int:
        with self._con.cursor() as cursor:
            self._execute(cursor, sql, args)
            self._con.commit()

            return cursor.rowcount

    def select(self, sql: str, *args: Any) -> Iterator[dict]:
        with self._con.cursor() as cursor:
            self._execute(cursor, sql, args)
            rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        for row in rows:
            yield dict(zip(columns, row))

    def procedure(self, func_name: str, **parameters: Any) -> int:
        sql = self._exec_sql(func_name, parameters)

        return self.perform(sql, *parameters.values())

    def function(self, func_name: str, **parameters: Any) -> Iterator[dict]:
        sql = self._exec_sql(func_name, parameters)

        return self.select(sql, *parameters.values())

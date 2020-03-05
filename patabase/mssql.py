import pyodbc


class Database(object):
    def __init__(self, server: str, user: str, password: str, database: str):
        self._con = pyodbc.connect(
            '',
            driver='SQL Server',
            server=server,
            user=user,
            password=password,
            database=database)

    def _execute(self, cursor, query, parameters):
        try:
            cursor.execute(query, parameters)
        except Exception as e:
            self._con.rollback()
            raise e

    @staticmethod
    def _exec_sql(func_name: str, parameters: dict) -> str:
        args = [f'@{k}=?' for k in parameters]

        sql = f'''
            exec {func_name} {''.join(args)}
        '''

        return sql

    def perform(self, sql: str, *args: any) -> int:
        with self._con.cursor() as cursor:
            self._execute(cursor, sql, args)
            self._con.commit()

            return cursor.rowcount

    def select(self, sql: str, *args: any) -> iter:
        with self._con.cursor() as cursor:
            self._execute(cursor, sql, args)
            rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        for row in rows:
            yield dict(zip(columns, row))

    def procedure(self, func_name: str, **parameters: any) -> int:
        sql = self._exec_sql(func_name, parameters)

        return self.perform(sql, *parameters.values())

    def function(self, func_name: str, **parameters: any) -> iter:
        sql = self._exec_sql(func_name, parameters)

        return self.select(sql, *parameters.values())

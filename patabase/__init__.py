try:
    from .mssql import Database as Mssql
except ModuleNotFoundError:
    from .empty import Database as Mssql

try:
    from .postgres import Database as Postgres
except ModuleNotFoundError:
    from .empty import Database as Postgres

__version__ = '0.2.1'

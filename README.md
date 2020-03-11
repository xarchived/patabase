# Patabase
Database API as it described in [PEP 249](https://www.python.org/dev/peps/pep-0249/) is a comprehensive API. It's 
amazing and we can implement any advanced scenario with it. But for a simple task we don't need an advanced or
comprehensive tool. We just need a simple tool to do the job for us. After all we all agreed that "Simple is better than
complex."

## Installation
We'd like to support all the databases, but we don't like to install all the drivers of all the databases. So first of
all install and config your database driver then install corresponding python package:

```bash
pip install -U psycopg2  # for Postgres

pip install -U pyodbc  # for Microsoft SQL Server 
``` 

now you can install it from PyPi by following command:

```bash
pip install -U patabase
```

or if you prefer the latest development version, you can install it from the source:

```bash
git clone https://github.com/xurvan/redisary.git
cd redisary
python setup.py install
```

"""
Connects to a SQL database using pyodbc
"""
from sqlalchemy import create_engine

SERVER = 'ds-sqlserver-conciliation-report-sbsb2999.cmudv60w2kae.us-east-1.rds.amazonaws.com'
DATABASE = 'HousePricingDB'
USERNAME = 'admin'
PASSWORD = 'SendPass**8L4!SP01Nov'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

try:
    conn = pyodbc.connect(connectionString)
    SQL_QUERY = """
    SELECT HouseID,Address FROM simulacro_saberpro.Houses;
    """
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    records = cursor.fetchall()
    for r in records:
        print(f"{r.codigo}\t{r.nombre}")
except Exception as e:
    print("An error ocurred:", e)

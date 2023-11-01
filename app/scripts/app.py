"""
Connects to a SQL database using pyodbc
"""
import pyodbc

SERVER = 'DSTK-ALEJANDRO-'
DATABASE = 'simulacro_saberpro'
USERNAME = 'admin_simulacro'
PASSWORD = 'simulacro_userdev23'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

try:
    conn = pyodbc.connect(connectionString)
    SQL_QUERY = """
    SELECT codigo,nombre FROM simulacro_saberpro.ciudad;
    """
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    records = cursor.fetchall()
    for r in records:
        print(f"{r.codigo}\t{r.nombre}")
except Exception as e:
    print("An error ocurred:", e)

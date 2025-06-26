print("On est dans collecte !")

# if you get this error : ModuleNotFoundError: No module named 'MySQLdb'
# Try this in your terminal: pip install mysqlclient

import pandas as pd
from sqlalchemy import create_engine, text
import time
import sys

# MySQL connection details
mysql_user = "root"
mysql_password = ""
mysql_db_name = "sciencestreaming"
mysql_port = 3306
# mysql_host = "127.0.0.1"
mysql_host = "mysql"  # Use Docker Compose service name
mysql_connection_string = f"mysql+mysqldb://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db_name}"
mysql_engine = create_engine(mysql_connection_string)

# PostgreSQL connection details
postgres_user = "postgres"
postgres_password = "pw"
postgres_db_name = "sciencestreaming_data_env"
postgres_port = 5432
# postgres_host = "127.0.0.1"
postgres_host = "postgres"  # Use Docker Compose service name
postgres_connection_string = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}"
postgres_engine = create_engine(postgres_connection_string)

# Convert sql query results to pandas DataFrame
def q(query, engine):
    with engine.begin() as conn:
        return pd.read_sql_query(text(query), conn)

# Function to fetch data from MySQL
def fetch_data_from_mysql(table_name, engine=mysql_engine):
    query = f"SELECT * FROM {table_name};"
    with engine.begin() as conn:
        return pd.read_sql_query(text(query), conn)

# Function to insert data into PostgreSQL
def insert_data_into_postgres(df, table_name, engine=postgres_engine):
    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Data from table '{table_name}' inserted into PostgreSQL.")

# Wait for MySQL to be ready
max_retries = 30
for i in range(max_retries):
    try:
        with mysql_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("MySQL is ready!")
        break
    except Exception as e:
        print(f"Waiting for MySQL to be ready... ({i+1}/{max_retries})")
        time.sleep(2)
else:
    print("MySQL is not ready after waiting. Exiting.")
    sys.exit(1)

# List of tables to transfer
tables = q("show tables;", mysql_engine).iloc[:,0].tolist()
# tables = ['course', 'sub', 'user', 'schedule', 'view', 'teacher']

# Transfer data from MySQL to PostgreSQL
for table in tables:
    print(f"Processing table: {table}")
    # Fetch data from MySQL
    df = fetch_data_from_mysql(table)
    if not df.empty:
        # Insert data into PostgreSQL
        insert_data_into_postgres(df, table)
    else:
        print(f"Table '{table}' is empty. Skipping.")
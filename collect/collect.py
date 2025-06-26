print("On est dans collecte !")

import pandas as pd
from sqlalchemy import create_engine, text

# MySQL connection details
mysql_user = "root"
mysql_password = ""
mysql_db_name = "sciencestreaming"
mysql_port = 3306
mysql_host = "127.0.0.1"
mysql_connection_string = f"mysql+mysqldb://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db_name}"
mysql_engine = create_engine(mysql_connection_string)

# PostgreSQL connection details
postgres_user = "postgres"
postgres_password = "pw"
postgres_db_name = "sciencestreaming_data_env"
postgres_port = 5432
postgres_host = "127.0.0.1"
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
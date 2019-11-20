from configparser import ConfigParser
from pathlib import Path

import psycopg2

configuration_path = Path("../configuration.conf")

configuration = ConfigParser()
configuration.read(configuration_path)

sql_conf = configuration["sql"]

connection = None
try:
    connection = psycopg2.connect(user=sql_conf["user"],
                                  password=sql_conf["password"],
                                  port=int(sql_conf["port"]),
                                  database=sql_conf["database"])

    query = open('init_db.sql', 'r').read()
    cursor = connection.cursor()
    # Create table - machine_stats
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("database initialized")
finally:
    if connection is not None:
        connection.close()

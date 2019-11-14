import logging

import psycopg2


class SqlWriter:
    def __init__(self, configuration):
        self.configuration = configuration

    def get_connection(self):
        return psycopg2.connect(user=self.configuration["user"],
                                password=self.configuration["password"],
                                port=int(self.configuration["port"]),
                                database=self.configuration["database"])

    def update_loading_rate(self, machine_id, time_stamp, load_rate, mileage):
        logging.debug("updating machine_statistic table")
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO machine_statistic (machine_id, timestamp, load_rate, mileage)
            VALUES (%s,%s,%s, %s)
        """,
                       (machine_id, time_stamp, load_rate, mileage))

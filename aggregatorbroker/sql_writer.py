import logging

from sqlalchemy import create_engine
from pandas import DataFrame


class SqlWriter:
    """
    class that handles writing to an SQL database.
    """
    def __init__(self, configuration):
        self.configuration = configuration
        dialect = configuration["dialect"]
        user = configuration["user"]
        password = configuration["password"]
        host = configuration["host"]
        port = configuration["port"]
        database = configuration["database"]
        self.table = configuration["table"]
        self.engine = create_engine(dialect + "://" + user + ":" + password + "@" + host + ":" + port + "/" + database,
                                    echo=False)

    def write(self, df: DataFrame):
        """
        Append the data frame data to the SQL table
        :param df: the data frame to append
        """
        logging.debug("updating {} table with data".format(self.table))
        # not the most efficient way to write to the database. see NOTES.md for other possibilities
        df.to_sql(self.table, self.engine, if_exists='append')

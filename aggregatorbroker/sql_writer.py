import logging

from sqlalchemy import create_engine


class SqlWriter:
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

    def write(self, aggregated_data):
        logging.debug("updating {} table with aggregated".format(self.table))
        # not the most efficient way to write to the database. see NOTES.md for other possibilities
        aggregated_data.to_sql(self.table, self.engine, if_exists='append')

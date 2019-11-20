import logging.config
from configparser import ConfigParser

import aggregatorbroker as agbro

if __name__ == '__main__':
    # logging
    logging.config.fileConfig('logging.conf')

    logging.info("start aggregator broker")

    # configuration
    configuration = ConfigParser()
    configuration.read("configuration.conf")

    # run the aggregator broket
    sql_writer = agbro.SqlWriter(configuration["sql"])
    handler = agbro.AggregatorHandler(configuration["handler"], sql_writer)
    mqtt_client = agbro.MqttClient(configuration["mqtt"], handler)

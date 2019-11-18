import logging.config
from configparser import ConfigParser

import aggregatorbroker as agbro

if __name__ == '__main__':
    # logging
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    # configuration
    configuration = ConfigParser()
    configuration.read("configuration.conf")

    sql_writer = agbro.SqlWriter(configuration["sql"])
    handler = agbro.AggregatorHandler(sql_writer)
    mqtt_client = agbro.MqttClient(configuration["mqtt"], handler)

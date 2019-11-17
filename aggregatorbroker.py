import logging.config
from configparser import ConfigParser

import aggregatorbrocker as agbro

if __name__ == '__main__':
    # logging
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    # configuration
    configuration = ConfigParser()
    configuration.read("configuration.conf")

    mqtt_client = agbro.MqttClient(configuration["mqtt"])
    sql_writer = agbro.SqlWriter(configuration["sql"])

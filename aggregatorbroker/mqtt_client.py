import logging

import paho.mqtt.client as mqtt

from constants import *
import utils


class MqttClient:
    """
    Class that wrap the MQTT client and defines the configration and the callbacks of the message broker
    """

    def __init__(self, configuration, message_handler):
        self.configuration = configuration
        self.message_handler = message_handler
        self.client = self._configure_client()
        self.client.loop_forever()

    def _configure_client(self):
        """
        Method that creates and configures the MQTT client
        :return the MQTT client
        """
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.connect(self.configuration[HOST], int(self.configuration[PORT]))
        return client

    def _on_connect(self, client, userdata, flags, rc):
        """
        Defines the on_connect callback for the MQTT client
        """
        logging.info("Connected with result code " + str(rc))
        topic = self.configuration[TOPIC]
        logging.info("Subscribing to " + topic)
        client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        """
        Defines the on_message callback for the MQTT client
        """
        ts_reception = utils.now()  # maybe we could use msg.timestamp?
        logging.getLogger(__name__).debug(msg.topic + " " + str(msg.payload))
        self.message_handler.handle_message(ts_reception, msg.payload)

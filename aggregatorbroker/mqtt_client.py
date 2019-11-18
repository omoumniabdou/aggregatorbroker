import logging

import paho.mqtt.client as mqtt

import utils


class MqttClient:
    def __init__(self, configuration, message_handler):
        self.configuration = configuration
        self.message_handler = message_handler
        self.client = self._configure_client()
        self.client.loop_forever()

    def _configure_client(self):
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.connect(self.configuration["host"], int(self.configuration["port"]))
        return client

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code " + str(rc))
        topic = self.configuration["topic"]
        logging.info("Subscribing to " + topic)
        client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        ts_reception = utils.now()  # maybe we could use msg.timestamp?
        logging.getLogger('mqtt_client').debug(msg.topic + " " + str(msg.payload))
        self.message_handler.handle_message(ts_reception, msg.payload)

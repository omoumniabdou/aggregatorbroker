import logging

import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, configuration):
        self.configuration = configuration
        self.client = self._configure_client()

    def _configure_client(self):
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.connect(self.configuration["host"], int(self.configuration["port"]))
        client.loop_forever()
        return client

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code " + str(rc))
        topic = self.configuration["topic"]
        logging.info("Subscribing to " + topic)
        client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        ts_reception = msg.timestamp  # maybe we could use msg.timestamp?
        logging.debug(msg.topic + " " + str(msg.payload))
